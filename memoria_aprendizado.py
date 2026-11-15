"""
Sistema de Memória e Aprendizado do Bastião
Permite que ele aprenda com as conversas e busque informações quando necessário
"""
import json
import os
from datetime import datetime
from pathlib import Path

class MemoriaBastiao:
    """Sistema de memória persistente para o Bastião"""
    
    def __init__(self, arquivo_memoria='memoria_bastiao.json'):
        self.arquivo = arquivo_memoria
        self.memoria = self._carregar_memoria()
    
    def _carregar_memoria(self):
        """Carrega memória do arquivo"""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._memoria_inicial()
        return self._memoria_inicial()
    
    def _memoria_inicial(self):
        """Estrutura inicial da memória"""
        return {
            'aprendizados': [],  # Coisas que aprendeu
            'pessoas': {},       # Informações sobre usuários
            'topicos': {},       # Conhecimentos por tópico
            'historias': [],     # Histórias contadas
            'ultima_atualizacao': datetime.now().isoformat()
        }
    
    def salvar(self):
        """Salva memória no arquivo"""
        self.memoria['ultima_atualizacao'] = datetime.now().isoformat()
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.memoria, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar memória: {e}")
            return False
    
    def adicionar_aprendizado(self, topico, informacao, fonte='conversa'):
        """Adiciona um novo aprendizado"""
        aprendizado = {
            'topico': topico,
            'informacao': informacao,
            'fonte': fonte,
            'data': datetime.now().isoformat()
        }
        
        self.memoria['aprendizados'].append(aprendizado)
        
        # Adiciona também ao índice de tópicos
        if topico not in self.memoria['topicos']:
            self.memoria['topicos'][topico] = []
        
        self.memoria['topicos'][topico].append(informacao)
        
        # Mantém apenas últimos 100 aprendizados
        if len(self.memoria['aprendizados']) > 100:
            self.memoria['aprendizados'] = self.memoria['aprendizados'][-100:]
        
        self.salvar()
    
    def buscar_conhecimento(self, topico):
        """Busca conhecimento sobre um tópico"""
        topico_lower = topico.lower()
        
        # Busca no índice de tópicos
        for key, valor in self.memoria['topicos'].items():
            if topico_lower in key.lower():
                return valor
        
        return None
    
    def lembrar_pessoa(self, usuario, informacao):
        """Lembra informação sobre uma pessoa"""
        if usuario not in self.memoria['pessoas']:
            self.memoria['pessoas'][usuario] = {
                'primeira_conversa': datetime.now().isoformat(),
                'informacoes': []
            }
        
        self.memoria['pessoas'][usuario]['informacoes'].append({
            'info': informacao,
            'data': datetime.now().isoformat()
        })
        
        self.salvar()
    
    def buscar_pessoa(self, usuario):
        """Busca informações sobre uma pessoa"""
        return self.memoria['pessoas'].get(usuario, None)
    
    def contar_aprendizados(self):
        """Retorna número de aprendizados"""
        return len(self.memoria['aprendizados'])
    
    def ultimos_aprendizados(self, n=5):
        """Retorna últimos N aprendizados"""
        return self.memoria['aprendizados'][-n:]
    
    def limpar_memoria(self):
        """Limpa toda a memória (usar com cuidado!)"""
        self.memoria = self._memoria_inicial()
        self.salvar()


class SistemaBuscaAprendizado:
    """Sistema que decide quando buscar informação e como aprender"""
    
    def __init__(self, memoria):
        self.memoria = memoria
    
    def precisa_buscar(self, pergunta):
        """
        Analisa se a pergunta requer busca de informação
        
        Returns:
            (precisa_buscar: bool, topico: str, razao: str)
        """
        pergunta_lower = pergunta.lower()
        
        # Palavras-chave que indicam necessidade de busca
        indicadores_busca = [
            ('o que é', 'definicao'),
            ('quem é', 'pessoa'),
            ('como funciona', 'explicacao'),
            ('quando foi', 'data_historica'),
            ('onde fica', 'localizacao'),
            ('qual é', 'informacao'),
            ('me explica', 'explicacao'),
            ('você sabe sobre', 'conhecimento'),
            ('já ouviu falar', 'conhecimento')
        ]
        
        for indicador, tipo in indicadores_busca:
            if indicador in pergunta_lower:
                # Extrai o tópico da pergunta
                topico = pergunta_lower.split(indicador)[1].strip('? ')
                return (True, topico, tipo)
        
        return (False, None, None)
    
    def buscar_informacao_web(self, topico):
        """
        Busca informação na web sobre um tópico
        
        Returns:
            (sucesso: bool, informacao: str)
        """
        try:
            # Tenta importar hermes_tools para web_search
            from hermes_tools import web_search, web_extract
            
            # Busca na web
            print(f"🔍 Bastião buscando sobre: {topico}")
            
            # Adiciona contexto gaúcho à busca se relevante
            query = topico
            if any(palavra in topico.lower() for palavra in ['tradição', 'gaúcho', 'mate', 'churrasco', 'rs', 'sul']):
                query = f"{topico} rio grande do sul gaúcho"
            
            resultados = web_search(query, limit=3)
            
            if resultados and 'data' in resultados and 'web' in resultados['data']:
                urls = [r['url'] for r in resultados['data']['web'][:2]]
                
                # Extrai conteúdo
                conteudo = web_extract(urls, char_limit=5000)
                
                if conteudo and 'results' in conteudo:
                    # Pega primeiro resultado com conteúdo
                    for resultado in conteudo['results']:
                        if resultado.get('content') and not resultado.get('error'):
                            # Pega primeiros 500 caracteres
                            info = resultado['content'][:500].strip()
                            return (True, info)
            
            return (False, "Não consegui encontrar informação confiável")
            
        except Exception as e:
            print(f"Erro na busca web: {e}")
            return (False, f"Erro ao buscar: {e}")
    
    def formatar_resposta_aprendizado(self, topico, informacao, tom_veterano=True):
        """
        Formata a resposta quando aprendeu algo novo
        """
        if tom_veterano:
            prefixos = [
                f"Bah guri, deixa eu te contar o que sei sobre {topico}...",
                f"Opa, sobre {topico}, deixa eu ver o que aprendi...",
                f"Bah, {topico}? Deixa eu pesquisar na memória aqui...",
                f"Sobre {topico}, guri, olha só o que descobri..."
            ]
        else:
            prefixos = [
                f"Sobre {topico}:",
                f"Deixa eu te contar sobre {topico}:",
                f"Olha só o que sei sobre {topico}:"
            ]
        
        import random
        prefixo = random.choice(prefixos)
        
        # Resume a informação
        resumo = informacao[:300] if len(informacao) > 300 else informacao
        
        sufixos = [
            "\n\nAgora sei mais uma coisa tchê!",
            "\n\nAprendi isso agora, bah!",
            "\n\nMais um aprendizado pros meus 70 anos!",
            "\n\nNunca é tarde pra aprender tchê!"
        ]
        
        sufixo = random.choice(sufixos) if tom_veterano else ""
        
        return f"{prefixo}\n\n{resumo}{sufixo}"
