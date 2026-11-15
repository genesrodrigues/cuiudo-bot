"""
Integração do Bastião com o Hermes (LLM local do usuário).

Fluxo:
  1. Filtro de segurança (assunto técnico -> desconversa, sem chamar o modelo)
  2. Monta o prompt: personalidade + memória relevante + conversa recente + mensagem
  3. Chama o Hermes (`hermes chat -q`, sem ferramentas) -> resposta como pessoa
  4. Se o modelo responder "[BUSCAR: termo]" é porque não sabe: busca na web,
     guarda na memória e chama o modelo de novo com a informação
  5. Se o Hermes falhar, cai no gerador de respostas por padrões (fallback)
"""
import asyncio
import os
import random
import re
import subprocess
import tempfile

from personalidade import PersonalidadeGaucha
from memoria_aprendizado import MemoriaBastiao
from gerador_respostas import GeradorRespostas


MARCADOR_BUSCA = re.compile(r'\[BUSCAR:\s*(.+?)\]', re.IGNORECASE)
MARCADOR_LEMBRAR = re.compile(r'\[LEMBRAR:\s*([^|\]]+?)\s*\|\s*(.+?)\]', re.IGNORECASE)

INSTRUCAO_BUSCA = """
QUANDO NÃO SOUBER:
Se te perguntarem um fato concreto que tu realmente não sabe (uma pessoa famosa, lugar, acontecimento recente,
termo que nunca ouviu), responde SOMENTE com [BUSCAR: termo a pesquisar] e mais nada.
Não usa isso pra opinião, conversa, convite, nem pra gente do servidor (sobre o pessoal tu usa o que tá listado e o que lembra). Na dúvida, responde normal.

O PESSOAL DO SERVIDOR:
Tu enxerga quem tá no servidor (lista abaixo quando tiver). Pode falar deles, comentar quem tá online, quem sumiu,
quem entrou faz pouco, chamar alguém pela conversa, puxar assunto com quem tá quieto. Trata todo mundo como conhecido da bodega.
Não inventa fato sobre ninguém: só usa o que tá na lista, na conversa, ou nas lembranças. Não zomba de ninguém de forma pesada.

LEMBRAR DAS PESSOAS:
Quando alguém contar algo pessoal digno de guardar (de onde é, o que faz, o que gosta, time, família, apelido, um causo),
acrescenta NO FINAL da resposta, em linha separada, [LEMBRAR: Nome | fato curto]. Pode ter mais de uma. Isso não aparece pra ninguém."""


class HermesIntegration:
    """Faz o Bastião responder usando o modelo configurado no Hermes."""

    def __init__(self, verbose=False, timeout=90):
        self.verbose = verbose
        self.timeout = timeout
        self.personalidade = PersonalidadeGaucha()
        self.memoria = MemoriaBastiao()
        self.gerador = GeradorRespostas()
        self.historico_conversa = []
        self.max_historico = 12
        self.hermes_ok = True  # vira False se o CLI não existir

        if verbose:
            print(f"📚 Memória carregada: {self.memoria.contar_aprendizados()} aprendizados")

    # ------------------------------------------------------------------ API
    async def processar_mensagem_async(self, mensagem_usuario, usuario=None, contexto_servidor=None):
        """Versão assíncrona: não trava o bot enquanto o modelo pensa."""
        return await asyncio.to_thread(self.processar_mensagem, mensagem_usuario, usuario, contexto_servidor)

    def processar_mensagem(self, mensagem_usuario, usuario=None, contexto_servidor=None):
        usuario = usuario or 'Alguém'
        self._ctx_servidor = contexto_servidor or {}

        seguro, resposta_desvio = self.personalidade.filtrar_seguranca(mensagem_usuario)
        if not seguro:
            self._adicionar_historico(mensagem_usuario, resposta_desvio, usuario)
            return resposta_desvio

        resposta = None
        if self.hermes_ok:
            contexto = self._montar_contexto(mensagem_usuario, usuario)
            resposta = self._chamar_hermes(contexto)

            # O modelo disse que não sabe -> busca, aprende, responde de novo
            if resposta:
                m = MARCADOR_BUSCA.search(resposta)
                if m:
                    termo = m.group(1).strip()
                    if self.verbose:
                        print(f"🔍 Bastião não sabe '{termo}', buscando...")
                    info = self._buscar_na_web(termo)
                    if info:
                        self.memoria.adicionar_aprendizado(termo, info, fonte='web')
                    contexto = self._montar_contexto(
                        mensagem_usuario, usuario,
                        info_nova=(termo, info) if info else (termo, None)
                    )
                    resposta = self._chamar_hermes(contexto)
                    resposta = MARCADOR_BUSCA.sub('', resposta or '').strip() or None

            # Guarda o que ele aprendeu sobre as pessoas e tira o marcador do texto
            if resposta:
                resposta = self._extrair_lembrancas(resposta)

        if not resposta:
            if self.verbose:
                print("⚠️ Hermes indisponível, usando gerador de padrões")
            resposta, _ = self.gerador.gerar_resposta(mensagem_usuario, usuario)

        self._adicionar_historico(mensagem_usuario, resposta, usuario)
        return resposta

    def _extrair_lembrancas(self, resposta):
        for nome, fato in MARCADOR_LEMBRAR.findall(resposta):
            nome, fato = nome.strip().lstrip('@'), fato.strip()
            if nome and fato:
                self.memoria.lembrar_pessoa(nome, fato)
                if self.verbose:
                    print(f"🧠 Lembrando: {nome} -> {fato}")
        return MARCADOR_LEMBRAR.sub('', resposta).strip() or None

    # ------------------------------------------------------------ contexto
    def _montar_contexto(self, mensagem, usuario, info_nova=None):
        partes = [self.personalidade.SYSTEM_PROMPT, INSTRUCAO_BUSCA]

        servidor = self._texto_servidor(mensagem, usuario)
        if servidor:
            partes.append(servidor)

        lembrancas = self._memoria_relevante(mensagem)
        if lembrancas:
            partes.append("\nCOISAS QUE TU APRENDEU CONVERSANDO COM O PESSOAL (usa se vier ao caso):\n" + lembrancas)

        if info_nova:
            termo, info = info_nova
            if info:
                partes.append(
                    f"\nTu acabou de perguntar pro Pedrinho / dar uma olhada e descobriu isto sobre \"{termo}\":\n{info}\n"
                    "Responde a pergunta com essa informação, do teu jeito, em poucas frases, "
                    "como quem acabou de ficar sabendo. Não usa [BUSCAR] de novo."
                )
            else:
                partes.append(
                    f"\nTu tentou descobrir sobre \"{termo}\" mas não achou nada. "
                    "Diz com naturalidade que não sabe e puxa outro assunto. Não usa [BUSCAR] de novo."
                )

        if self.historico_conversa:
            partes.append("\nCONVERSA RECENTE NO GRUPO:")
            for msg in self.historico_conversa[-8:]:
                partes.append(f"{msg['usuario']}: {msg['mensagem']}")
                partes.append(f"Bastião: {msg['resposta']}")

        partes.append(f"\nAGORA {usuario} te mandou:\n{mensagem}\n\nBastião responde:")
        return "\n".join(partes)

    def _texto_servidor(self, mensagem, usuario):
        """Descreve o servidor, os membros e o que lembra de cada um."""
        ctx = self._ctx_servidor
        linhas = []
        if ctx.get('servidor'):
            canal = f", canal #{ctx['canal']}" if ctx.get('canal') else ""
            linhas.append(f"\nSERVIDOR: \"{ctx['servidor']}\"{canal}, {ctx.get('total_membros', len(ctx.get('membros', [])))} pessoas.")

        membros = ctx.get('membros', [])
        nomes_membros = {m['nome'] for m in membros}
        if membros:
            linhas.append("QUEM TÁ NO SERVIDOR (nome - status - detalhes):")
            for m in membros:
                extras = []
                if m.get('dono'):
                    extras.append("dono do servidor")
                if m.get('cargos'):
                    extras.append("cargo: " + ", ".join(m['cargos']))
                if m.get('fazendo'):
                    extras.append("agora: " + m['fazendo'])
                if m.get('entrou'):
                    extras.append("entrou em " + m['entrou'])
                linhas.append(f"- {m['nome']} - {m['status']}" + (" - " + "; ".join(extras) if extras else ""))

        # Lembranças: do autor + de quem for citado na mensagem + de quem tá na lista
        texto_lower = mensagem.lower()
        citados = {usuario}
        for nome in list(nomes_membros) + list(self.memoria.memoria.get('pessoas', {}).keys()):
            if nome.lower() in texto_lower:
                citados.add(nome)
        lembr = []
        for nome in citados:
            p = self.memoria.buscar_pessoa(nome)
            if p and p.get('informacoes'):
                fatos = [i['info'] for i in p['informacoes'][-6:]]
                lembr.append(f"- {nome}: " + "; ".join(fatos))
        if lembr:
            linhas.append("O QUE TU LEMBRA DESSAS PESSOAS:")
            linhas.extend(lembr)

        if ctx.get('conversa_recente'):
            linhas.append("ÚLTIMAS MENSAGENS NO CANAL (antes da atual):")
            linhas.extend(ctx['conversa_recente'])

        return "\n".join(linhas) if linhas else ""

    def _memoria_relevante(self, mensagem):
        palavras = {p for p in re.findall(r'\w{4,}', mensagem.lower())}
        achados = []
        for topico, infos in self.memoria.memoria.get('topicos', {}).items():
            t = topico.lower()
            if any(p in t or t in p for p in palavras):
                achados.append(f"- {topico}: {infos[-1][:300]}")
            if len(achados) >= 3:
                break
        return "\n".join(achados)

    # --------------------------------------------------------------- hermes
    def _chamar_hermes(self, contexto):
        """Roda `hermes chat` sem ferramentas e devolve só a fala do Bastião."""
        tmpdir = os.environ.get('TMPDIR') or tempfile.gettempdir()
        try:
            with tempfile.NamedTemporaryFile('w', suffix='.txt', dir=tmpdir, delete=False, encoding='utf-8') as f:
                f.write(contexto)
                caminho = f.name
        except Exception as e:
            if self.verbose:
                print(f"Erro criando arquivo de prompt: {e}")
            return None

        try:
            result = subprocess.run(
                ['hermes', 'chat', '--query-file', caminho, '-Q',
                 '-t', '', '--reasoning', 'none', '--max-turns', '1'],
                capture_output=True, text=True, encoding='utf-8', errors='replace',
                timeout=self.timeout, shell=(os.name == 'nt')
            )
        except FileNotFoundError:
            self.hermes_ok = False
            if self.verbose:
                print("❌ comando 'hermes' não encontrado no PATH")
            return None
        except subprocess.TimeoutExpired:
            if self.verbose:
                print("⏱️ Hermes demorou demais")
            return None
        except Exception as e:
            if self.verbose:
                print(f"Erro ao chamar Hermes: {e}")
            return None
        finally:
            try:
                os.unlink(caminho)
            except OSError:
                pass

        if result.returncode != 0:
            if self.verbose:
                print(f"Hermes retornou erro: {result.stderr[-500:]}")
            return None

        return self._limpar_resposta(result.stdout)

    @staticmethod
    def _limpar_resposta(texto):
        linhas = []
        for linha in texto.splitlines():
            if linha.strip().lower().startswith('session_id:'):
                continue
            linhas.append(linha)
        resposta = "\n".join(linhas).strip()
        resposta = re.sub(r'^(Bastião|Assistant)\s*:\s*', '', resposta, flags=re.IGNORECASE).strip()
        if len(resposta) >= 2 and resposta[0] == resposta[-1] == '"':
            resposta = resposta[1:-1].strip()
        # Discord limita a 2000 caracteres
        return resposta[:1900] if resposta else None

    # ----------------------------------------------------------------- busca
    def _buscar_na_web(self, termo):
        """Tenta hermes_tools; senão Wikipédia (pt) e DuckDuckGo via urllib. Devolve texto curto ou None."""
        texto = self._buscar_hermes_tools(termo)
        if not texto:
            texto = self._buscar_wikipedia(termo)
        if not texto:
            texto = self._buscar_duckduckgo(termo)
        if self.verbose:
            print("✅ achei algo" if texto else "❌ não achei nada")
        return texto

    def _buscar_hermes_tools(self, termo):
        try:
            from hermes_tools import web_search, web_extract
        except ImportError:
            return None
        try:
            res = web_search(termo, limit=3)
            itens = (res or {}).get('data', {}).get('web', [])
            trechos = [f"{i.get('title','')}: {i.get('description','')}" for i in itens if i.get('description')]
            urls = [i['url'] for i in itens[:2] if i.get('url')]
            if urls:
                ext = web_extract(urls, char_limit=2500)
                for r in (ext or {}).get('results', []):
                    if r.get('content') and not r.get('error'):
                        trechos.append(r['content'][:800])
                        break
            texto = "\n".join(trechos).strip()
            return texto[:1200] if texto else None
        except Exception as e:
            if self.verbose:
                print(f"Erro na busca (hermes_tools): {e}")
            return None

    @staticmethod
    def _http_get(url, timeout=15):
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'BastiaoBot/1.0 (discord bot; contato local)'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='replace')

    def _buscar_wikipedia(self, termo):
        import json
        import urllib.parse
        for lang in ('pt', 'en'):
            try:
                q = urllib.parse.urlencode({'action': 'query', 'list': 'search', 'srsearch': termo,
                                            'format': 'json', 'srlimit': 1, 'utf8': 1})
                data = json.loads(self._http_get(f"https://{lang}.wikipedia.org/w/api.php?{q}"))
                hits = data.get('query', {}).get('search', [])
                if not hits:
                    continue
                titulo = hits[0]['title']
                resumo = json.loads(self._http_get(
                    f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(titulo)}"))
                extrato = (resumo.get('extract') or '').strip()
                if extrato:
                    return f"{titulo} (Wikipédia): {extrato}"[:1200]
            except Exception as e:
                if self.verbose:
                    print(f"Erro na busca (wikipedia {lang}): {e}")
        return None

    def _buscar_duckduckgo(self, termo):
        import html
        import urllib.parse
        try:
            pagina = self._http_get("https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({'q': termo}))
            trechos = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', pagina, flags=re.S)
            limpos = []
            for t in trechos[:4]:
                t = html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
                if t:
                    limpos.append(t)
            texto = "\n".join(limpos)
            return texto[:1200] if texto else None
        except Exception as e:
            if self.verbose:
                print(f"Erro na busca (duckduckgo): {e}")
            return None

    # ------------------------------------------------------------- histórico
    def _adicionar_historico(self, mensagem, resposta, usuario):
        self.historico_conversa.append({'usuario': usuario, 'mensagem': mensagem, 'resposta': resposta})
        self.historico_conversa = self.historico_conversa[-self.max_historico:]

    def limpar_historico(self):
        self.historico_conversa = []

    def estatisticas_aprendizado(self):
        return {
            'total_aprendizados': self.memoria.contar_aprendizados(),
            'topicos': len(self.memoria.memoria.get('topicos', {})),
            'pessoas': len(self.memoria.memoria.get('pessoas', {})),
        }


# Compatibilidade
class HermesDirectIntegration(HermesIntegration):
    pass
