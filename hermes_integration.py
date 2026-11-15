"""
Integração com Hermes para processamento local de mensagens
O Cuiudo usa Hermes para gerar respostas mantendo sua personalidade gaúcha
"""
import subprocess
import json
import tempfile
import os
from personalidade import PersonalidadeGaucha

class HermesIntegration:
    """Integra o Cuiudo com Hermes rodando localmente"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.personalidade = PersonalidadeGaucha()
        self.historico_conversa = []
        self.max_historico = 20  # Mantém últimas 20 mensagens
    
    def processar_mensagem(self, mensagem_usuario, usuario=None):
        """
        Processa uma mensagem usando Hermes localmente
        
        Args:
            mensagem_usuario: Texto da mensagem
            usuario: Nome do usuário (opcional)
        
        Returns:
            Resposta do Cuiudo
        """
        # Filtro de segurança - verifica se não é pergunta técnica
        seguro, resposta_desvio = self.personalidade.filtrar_seguranca(mensagem_usuario)
        if not seguro:
            return resposta_desvio
        
        # Monta contexto com personalidade
        contexto = self._montar_contexto(mensagem_usuario, usuario)
        
        try:
            # Chama Hermes via CLI
            resposta = self._chamar_hermes(contexto)
            
            # Adiciona ao histórico
            self._adicionar_historico(mensagem_usuario, resposta, usuario)
            
            # Garante sotaque gaúcho
            resposta_final = self.personalidade.adicionar_sotaque_gaucho(resposta)
            
            return resposta_final
            
        except Exception as e:
            if self.verbose:
                print(f"Erro ao chamar Hermes: {e}")
            
            # Fallback: resposta genérica gaúcha
            return self._resposta_fallback()
    
    def _montar_contexto(self, mensagem, usuario=None):
        """Monta o contexto da conversa para o Hermes"""
        # Monta histórico de conversa
        historico_texto = ""
        if self.historico_conversa:
            historico_texto = "\n\nCONVERSA RECENTE:\n"
            for msg in self.historico_conversa[-5:]:  # Últimas 5 mensagens
                historico_texto += f"{msg['usuario']}: {msg['mensagem']}\n"
                historico_texto += f"Cuiudo: {msg['resposta']}\n"
        
        # Contexto completo
        usuario_info = f" (usuário: {usuario})" if usuario else ""
        contexto = f"""{self.personalidade.SYSTEM_PROMPT}

{historico_texto}

MENSAGEM ATUAL{usuario_info}:
{mensagem}

Responda como o Cuiudo, mantendo sua personalidade gaúcha autêntica. Seja natural e use gírias gauchescas."""
        
        return contexto
    
    def _chamar_hermes(self, contexto):
        """
        Chama o Hermes CLI para processar a mensagem
        
        Nota: Este método usa hermes em modo one-shot local
        """
        try:
            # Cria arquivo temporário com o prompt
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
                f.write(contexto)
                temp_file = f.name
            
            try:
                # Chama hermes em modo one-shot
                # Usa o modelo configurado do usuário
                result = subprocess.run(
                    ['hermes', '--prompt', contexto, '--max-tokens', '150'],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    resposta = result.stdout.strip()
                    
                    # Remove possíveis prefixos do Hermes
                    resposta = resposta.replace('Assistant:', '').replace('Cuiudo:', '').strip()
                    
                    return resposta if resposta else self._resposta_fallback()
                else:
                    if self.verbose:
                        print(f"Hermes retornou erro: {result.stderr}")
                    return self._resposta_fallback()
                    
            finally:
                # Remove arquivo temporário
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except subprocess.TimeoutExpired:
            if self.verbose:
                print("Timeout ao chamar Hermes")
            return self._resposta_fallback()
        except FileNotFoundError:
            if self.verbose:
                print("Hermes não encontrado no PATH")
            return self._resposta_fallback()
        except Exception as e:
            if self.verbose:
                print(f"Erro inesperado: {e}")
            return self._resposta_fallback()
    
    def _resposta_fallback(self):
        """Retorna uma resposta genérica quando Hermes falha"""
        respostas = [
            "Bah tchê, me perdi no pensamento aqui! Me fala de novo?",
            "Opa, viajei tchê! Pode repetir?",
            "Barbaridade, tava pensando em outra coisa! O que tu disse?",
            "Bah, deu um branco aqui! Como é que é?",
            "Capaz, não entendi direito tchê! Explica de novo?",
            "Tri confuso isso aí, me explica melhor tchê!",
            "Bah, tô meio aéreo hoje! Repete aí?"
        ]
        return self.personalidade.pegar_giria('surpresa') + " " + random.choice(respostas)
    
    def _adicionar_historico(self, mensagem, resposta, usuario):
        """Adiciona interação ao histórico"""
        self.historico_conversa.append({
            'usuario': usuario or 'Alguém',
            'mensagem': mensagem,
            'resposta': resposta
        })
        
        # Mantém apenas as últimas N mensagens
        if len(self.historico_conversa) > self.max_historico:
            self.historico_conversa = self.historico_conversa[-self.max_historico:]
    
    def limpar_historico(self):
        """Limpa o histórico de conversas"""
        self.historico_conversa = []

# Versão alternativa: integração direta via Python
# Para quando o Hermes está disponível como módulo Python
class HermesDirectIntegration:
    """
    Integração direta com Hermes via import (se disponível)
    Fallback para CLI se não estiver disponível
    """
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.usar_cli = True
        
        # Tenta importar Hermes como módulo
        try:
            # Esta importação funcionará se Hermes estiver instalado como pacote Python
            # No momento, usamos CLI como padrão
            pass
        except ImportError:
            if verbose:
                print("Usando Hermes via CLI")
            self.usar_cli = True
        
        # Cria integração CLI
        self.cli_integration = HermesIntegration(verbose=verbose)
    
    def processar_mensagem(self, mensagem, usuario=None):
        """Processa mensagem usando o método disponível"""
        return self.cli_integration.processar_mensagem(mensagem, usuario)

import random
