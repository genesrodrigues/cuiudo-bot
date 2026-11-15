"""
Configurações do Cuiudo
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Credenciais Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')

# Configurações do bot
ACTIVITY_INTERVAL = int(os.getenv('CUIUDO_ACTIVITY_INTERVAL', '300'))  # 5 minutos
VERBOSE = os.getenv('CUIUDO_VERBOSE', 'false').lower() == 'true'

# Canal de boas-vindas (nome do canal onde enviar mensagens de boas-vindas)
WELCOME_CHANNEL_NAME = 'geral'  # Altere conforme seu servidor

# Prefixo de comandos (opcional - para comandos explícitos)
COMMAND_PREFIX = '!'

# Configurações de segurança
ALLOWED_TOPICS = [
    'chimarrão', 'churrasco', 'gaúcho', 'campo', 'mate', 'sul',
    'tradições', 'cultura', 'música', 'conversa', 'amizade',
    'clima', 'futebol', 'culinária', 'festa', 'baile'
]

BLOCKED_TOPICS = [
    'system', 'terminal', 'comando', 'executar', 'bash', 'shell',
    'arquivo', 'diretório', 'senha', 'token', 'credencial',
    'código', 'programação', 'técnico', 'servidor', 'host'
]
