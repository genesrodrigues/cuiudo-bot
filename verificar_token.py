"""
Script para testar o token do Discord
Execute para verificar se o token está correto ANTES de rodar o bot
"""
import sys
import os

# Tenta carregar o .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ python-dotenv não instalado!")
    print("   Execute: pip install python-dotenv")
    sys.exit(1)

def verificar_token():
    """Verifica se o token está configurado e parece válido"""
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 Verificador de Token Discord")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Verifica se .env existe
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        print("\nCrie o arquivo .env copiando .env.example:")
        print("   cp .env.example .env")
        return False
    
    # Pega o token
    token = os.getenv('DISCORD_TOKEN', '').strip()
    
    # Verifica se está vazio
    if not token:
        print("❌ Token não configurado no .env!")
        print("\nEdite o arquivo .env e adicione:")
        print("   DISCORD_TOKEN=seu_token_aqui")
        return False
    
    # Verifica se é o placeholder
    if 'COLE' in token.upper() or 'TOKEN' in token.upper() or 'AQUI' in token.upper():
        print("❌ Token ainda é placeholder!")
        print("\nVocê precisa substituir pelo token real do Discord.")
        print("Veja: ONDE_ESTA_O_TOKEN.txt")
        return False
    
    # Verifica se parece com Client Secret (curto demais)
    if len(token) < 50:
        print(f"⚠️  Token muito curto ({len(token)} caracteres)")
        print("\nIsso parece ser o Client Secret, não o Bot Token!")
        print("\n❌ VOCÊ ESTÁ USANDO A CREDENCIAL ERRADA!")
        print("\nO Bot Token tem ~70+ caracteres e dois pontos no meio.")
        print("Exemplo: MTU3MTQ4OTA3MDk1MjA5NTc0NA.GxYzAB.dQw4w9W...")
        print("\nVeja: ONDE_ESTA_O_TOKEN.txt")
        return False
    
    # Verifica formato básico do token Discord (tem dois pontos)
    pontos = token.count('.')
    if pontos < 2:
        print(f"⚠️  Formato de token inválido!")
        print("\nBot Token Discord tem duas partes separadas por pontos (.)")
        print("Exemplo: MTU3MTQ4OTA3MDk1MjA5NTc0NA.GxYzAB.dQw4w9W...")
        print("\nVocê pode ter copiado errado ou é a credencial errada.")
        print("Veja: ONDE_ESTA_O_TOKEN.txt")
        return False
    
    # Se passou todas as verificações básicas
    print("✅ Token encontrado!")
    print(f"   Tamanho: {len(token)} caracteres")
    print(f"   Formato: Parece válido (tem {pontos} pontos)")
    print(f"   Início: {token[:10]}...")
    
    # Tenta conectar (requer discord.py)
    print("\n🔄 Testando conexão com Discord...")
    
    try:
        import discord
        from discord.ext import commands
        
        # Cria um bot temporário apenas para testar
        intents = discord.Intents.default()
        bot = commands.Bot(command_prefix='!', intents=intents)
        
        @bot.event
        async def on_ready():
            print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"✅ TOKEN VÁLIDO!")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"   Bot: {bot.user.name}")
            print(f"   ID: {bot.user.id}")
            print(f"   Servidores: {len(bot.guilds)}")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"\nBah tchê! Token tá funcionando!")
            print(f"Pode rodar o Cuiudo: python cuiudo.py")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            await bot.close()
        
        # Tenta conectar
        import asyncio
        try:
            asyncio.run(bot.start(token))
            return True
        except discord.errors.LoginFailure:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("❌ TOKEN INVÁLIDO!")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("\nO token não foi aceito pelo Discord.")
            print("\nPossíveis causas:")
            print("  1. Token copiado errado (faltando partes)")
            print("  2. Token de outra aplicação")
            print("  3. Token foi resetado no Discord")
            print("\nSolução:")
            print("  1. Vá em: https://discord.com/developers/applications/1571489070952095744/bot")
            print("  2. Clique 'Reset Token'")
            print("  3. Copie o novo token completo")
            print("  4. Cole no .env")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            return False
            
    except ImportError:
        print("\n⚠️  discord.py não instalado - não foi possível testar conexão")
        print("   Execute: pip install -r requirements.txt")
        print("\n   Mas o formato do token parece OK!")
        print("   Você pode tentar rodar o bot mesmo assim.")
        return None

if __name__ == "__main__":
    resultado = verificar_token()
    
    if resultado is False:
        print("\n❌ Corrija o token antes de continuar!\n")
        sys.exit(1)
    elif resultado is None:
        print("\n⚠️  Instale as dependências para teste completo\n")
        sys.exit(0)
    else:
        sys.exit(0)
