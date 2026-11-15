"""
Integração com Hermes para processamento local de mensagens
O Bastião usa Hermes para gerar respostas mantendo sua personalidade gaúcha
Agora com sistema de aprendizado e busca de informações
"""
import subprocess
import json
import tempfile
import os
import random
from personalidade import PersonalidadeGaucha
from memoria_aprendizado import MemoriaBastiao, SistemaBuscaAprendizado

class HermesIntegration:
    """Integra o Bastião com Hermes rodando localmente + Sistema de Aprendizado"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.personalidade = PersonalidadeGaucha()
        self.historico_conversa = []
        self.max_historico = 20  # Mantém últimas 20 mensagens
        
        # Sistema de memória e aprendizado
        self.memoria = MemoriaBastiao()
        self.busca = SistemaBuscaAprendizado(self.memoria)
        
        if verbose:
            print(f"📚 Memória carregada: {self.memoria.contar_aprendizados()} aprendizados")
    
    def processar_mensagem(self, mensagem_usuario, usuario=None):
        """
        Processa uma mensagem usando Hermes localmente
        Agora com capacidade de buscar e aprender
        
        Args:
            mensagem_usuario: Texto da mensagem
            usuario: Nome do usuário (opcional)
        
        Returns:
            Resposta do Bastião
        """
        # Filtro de segurança - verifica se não é pergunta técnica
        seguro, resposta_desvio = self.personalidade.filtrar_seguranca(mensagem_usuario)
        if not seguro:
            return resposta_desvio
        
        # Verifica se precisa buscar informação
        precisa_buscar, topico, razao = self.busca.precisa_buscar(mensagem_usuario)
        
        if precisa_buscar and topico:
            # Primeiro verifica se já sabe sobre o tópico
            conhecimento_existente = self.memoria.buscar_conhecimento(topico)
            
            if conhecimento_existente:
                # Já sabe! Usa o conhecimento armazenado
                if self.verbose:
                    print(f"💡 Já sei sobre: {topico}")
                
                resposta = self._responder_com_conhecimento(topico, conhecimento_existente)
            else:
                # Não sabe - vai buscar!
                if self.verbose:
                    print(f"🔍 Não sei sobre '{topico}' - vou buscar!")
                
                resposta = self._buscar_e_aprender(topico, usuario)
        else:
            # Conversa normal
            contexto = self._montar_contexto(mensagem_usuario, usuario)
            
            try:
                # Chama Hermes via CLI (fallback)
                resposta = self._chamar_hermes(contexto)
                
                # Garante sotaque gaúcho
                resposta = self.personalidade.adicionar_sotaque_gaucho(resposta)
                
            except Exception as e:
                if self.verbose:
                    print(f"Erro ao chamar Hermes: {e}")
                resposta = self._resposta_fallback()
        
        # Adiciona ao histórico
        self._adicionar_historico(mensagem_usuario, resposta, usuario)
        
        return resposta
    
    def _buscar_e_aprender(self, topico, usuario=None):
        """Busca informação na web e aprende"""
        respostas_procurando = [
            f"Bah guri, deixa eu procurar sobre {topico}... Um minutinho!",
            f"Opa, {topico}? Nunca é tarde pra aprender! Deixa eu buscar...",
            f"Barbaridade, não sei sobre {topico}! Mas vou descobrir já!",
            f"Bah, {topico}... Com 70 anos ainda tem coisa que não sei! Vou buscar..."
        ]
        
        if self.verbose:
            print(random.choice(respostas_procurando))
        
        # Tenta buscar via hermes_tools
        try:
            from hermes_tools import web_search, web_extract
            
            # Monta query de busca
            query = topico
            if any(palavra in topico.lower() for palavra in ['gaúcho', 'mate', 'churrasco', 'rs', 'sul', 'tradição']):
                query = f"{topico} rio grande do sul gaúcho tradição"
            
            # Busca
            resultado_busca = web_search(query, limit=3)
            
            if resultado_busca and 'data' in resultado_busca and 'web' in resultado_busca['data']:
                urls = [r['url'] for r in resultado_busca['data']['web'][:2]]
                conteudo = web_extract(urls, char_limit=3000)
                
                if conteudo and 'results' in conteudo:
                    for item in conteudo['results']:
                        if item.get('content') and not item.get('error'):
                            info = item['content'][:600].strip()
                            
                            # Aprende!
                            self.memoria.adicionar_aprendizado(topico, info, fonte='web')
                            
                            if self.verbose:
                                print(f"✅ Aprendi sobre: {topico}")
                            
                            # Formata resposta de veterano
                            return self._formatar_aprendizado_gaucho(topico, info)
            
            # Se não encontrou nada útil
            return self._resposta_nao_encontrou(topico)
            
        except ImportError:
            # hermes_tools não disponível - resposta honesta
            return self._resposta_sem_busca(topico)
        except Exception as e:
            if self.verbose:
                print(f"Erro na busca: {e}")
            return self._resposta_erro_busca(topico)
    
    def _responder_com_conhecimento(self, topico, conhecimento):
        """Responde usando conhecimento já armazenado"""
        prefixos = [
            f"Bah, sobre {topico} eu já sei!",
            f"Opa, {topico}! Deixa eu ver aqui na memória...",
            f"Bah, {topico}... Já aprendi sobre isso!",
            f"Sobre {topico}, guri, olha só:"
        ]
        
        # Pega a informação mais recente
        info = conhecimento[-1] if isinstance(conhecimento, list) else conhecimento
        
        # Limita tamanho
        if len(info) > 400:
            info = info[:400] + "..."
        
        return f"{random.choice(prefixos)}\n\n{info}\n\nBah, bom ter isso na memória tchê!"
    
    def _formatar_aprendizado_gaucho(self, topico, informacao):
        """Formata a informação aprendida com tom de gaúcho de 70 anos"""
        prefixos = [
            f"Bah guri, olha só o que descobri sobre {topico}:",
            f"Opa! Aprendi sobre {topico} agora:",
            f"Barbaridade, que interessante esse {topico}!",
            f"Bah, nunca é tarde pra aprender! Sobre {topico}:"
        ]
        
        sufixos = [
            "\n\nAgora sei mais uma coisa tchê! Valeu por perguntar!",
            "\n\nBah, aprendi algo novo com meus 70 anos!",
            "\n\nGuardei isso na memória, guri!",
            "\n\nTri bom aprender coisas novas!"
        ]
        
        # Limita tamanho
        if len(informacao) > 400:
            informacao = informacao[:400] + "..."
        
        return f"{random.choice(prefixos)}\n\n{informacao}{random.choice(sufixos)}"
    
    def _resposta_nao_encontrou(self, topico):
        """Resposta quando não encontrou informação"""
        respostas = [
            f"Bah guri, procurei sobre {topico} mas não achei nada de confiável...",
            f"Opa, tentei buscar sobre {topico} mas não consegui informação boa tchê.",
            f"Barbaridade, não achei nada claro sobre {topico}... Desculpa guri!",
            f"Bah, sobre {topico} não encontrei informação que preste... Me pergunta outra coisa?"
        ]
        return random.choice(respostas)
    
    def _resposta_sem_busca(self, topico):
        """Resposta quando não pode buscar"""
        respostas = [
            f"Bah guri, sobre {topico} não sei não... E no momento não consigo buscar.",
            f"Opa, {topico}... Não sei tchê, e não tô podendo procurar agora.",
            f"Barbaridade, sobre {topico} não sei... Desculpa guri!"
        ]
        return random.choice(respostas)
    
    def _resposta_erro_busca(self, topico):
        """Resposta quando deu erro na busca"""
        respostas = [
            f"Bah, tentei buscar sobre {topico} mas deu problema tchê...",
            f"Opa, queria saber sobre {topico} mas deu erro aqui... Desculpa guri!",
            f"Barbaridade, tentei procurar {topico} mas não deu certo..."
        ]
        return random.choice(respostas)
    
    def _montar_contexto(self, mensagem, usuario=None):
        """Monta o contexto da conversa para o Hermes"""
        # Monta histórico de conversa
        historico_texto = ""
        if self.historico_conversa:
            historico_texto = "\n\nCONVERSA RECENTE:\n"
            for msg in self.historico_conversa[-5:]:  # Últimas 5 mensagens
                historico_texto += f"{msg['usuario']}: {msg['mensagem']}\n"
                historico_texto += f"Bastião: {msg['resposta']}\n"
        
        # Adiciona aprendizados recentes ao contexto
        aprendizados_texto = ""
        ultimos = self.memoria.ultimos_aprendizados(3)
        if ultimos:
            aprendizados_texto = "\n\nAPRENDIZADOS RECENTES:\n"
            for apr in ultimos:
                aprendizados_texto += f"- {apr['topico']}: {apr['informacao'][:100]}...\n"
        
        # Contexto completo
        usuario_info = f" (usuário: {usuario})" if usuario else ""
        contexto = f"""{self.personalidade.SYSTEM_PROMPT}

{historico_texto}{aprendizados_texto}

MENSAGEM ATUAL{usuario_info}:
{mensagem}

Responda como o Bastião, mantendo sua personalidade de gaúcho veterano de 70 anos."""
        
        return contexto
    
    def _chamar_hermes(self, contexto):
        """Chama o Hermes CLI para processar a mensagem (fallback)"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
                f.write(contexto)
                temp_file = f.name
            
            try:
                result = subprocess.run(
                    ['hermes', '--prompt', contexto, '--max-tokens', '200'],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    resposta = result.stdout.strip()
                    resposta = resposta.replace('Assistant:', '').replace('Bastião:', '').strip()
                    return resposta if resposta else self._resposta_fallback()
                else:
                    return self._resposta_fallback()
                    
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except Exception as e:
            if self.verbose:
                print(f"Erro ao chamar Hermes: {e}")
            return self._resposta_fallback()
    
    def _resposta_fallback(self):
        """Retorna uma resposta genérica quando falha"""
        respostas = [
            "Bah guri, me perdi no pensamento aqui... Me fala de novo?",
            "Opa, viajei tchê! Pode repetir?",
            "Barbaridade, tava pensando em outra coisa! O que tu disse?",
            "Bah, com 70 anos às vezes a memória falha... Como é que é?",
            "Capaz, não entendi direito tchê! Explica de novo?",
            "Bah, tô meio aéreo hoje! Repete aí?"
        ]
        return random.choice(respostas)
    
    def _adicionar_historico(self, mensagem, resposta, usuario):
        """Adiciona interação ao histórico"""
        self.historico_conversa.append({
            'usuario': usuario or 'Alguém',
            'mensagem': mensagem,
            'resposta': resposta
        })
        
        if len(self.historico_conversa) > self.max_historico:
            self.historico_conversa = self.historico_conversa[-self.max_historico:]
    
    def limpar_historico(self):
        """Limpa o histórico de conversas"""
        self.historico_conversa = []
    
    def estatisticas_aprendizado(self):
        """Retorna estatísticas de aprendizado"""
        return {
            'total_aprendizados': self.memoria.contar_aprendizados(),
            'topicos': len(self.memoria.memoria['topicos']),
            'pessoas': len(self.memoria.memoria['pessoas']),
            'ultimos_3': self.memoria.ultimos_aprendizados(3)
        }


# Versão alternativa mantida para compatibilidade
class HermesDirectIntegration:
    """Integração direta com Hermes via import (fallback para CLI)"""
    
    def __init__(self, verbose=False):
        self.cli_integration = HermesIntegration(verbose=verbose)
    
    def processar_mensagem(self, mensagem, usuario=None):
        """Processa mensagem usando o método disponível"""
        return self.cli_integration.processar_mensagem(mensagem, usuario)
