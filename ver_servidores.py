"""
Script para verificar em quais servidores o Cuiudo está
Conecta rapidamente e mostra informações
"""
import discord
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def verificar_servidores():
    """Conecta e lista servidores"""
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 Verificando servidores do Cuiudo...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("❌ Token não encontrado no .env!")
        return
    
    # Configuração mínima apenas para listar servidores
    intents = discord.Intents.default()
    intents.guilds = True  # Permissão para ver servidores
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"✅ Conectado como: {client.user.name} (ID: {client.user.id})\n")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📊 SERVIDORES: {len(client.guilds)}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        if len(client.guilds) == 0:
            print("⚠️  O bot NÃO está em nenhum servidor ainda!")
            print("\n📝 Para adicionar o bot a um servidor:\n")
            print("1. Vá em: https://discord.com/developers/applications/1571489070952095744/oauth2/url-generator")
            print("\n2. Selecione:")
            print("   Scopes: ☑️ bot")
            print("   Permissions: ☑️ Send Messages, ☑️ Read Messages")
            print("\n3. Copie a URL gerada e abra no navegador")
            print("4. Selecione o servidor e autorize\n")
        else:
            print("Servidores onde o Cuiudo está:\n")
            for i, guild in enumerate(client.guilds, 1):
                print(f"{i}. {guild.name}")
                print(f"   ID: {guild.id}")
                print(f"   Membros: {guild.member_count}")
                print(f"   Dono: {guild.owner}")
                print()
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        # Desconecta
        await client.close()
    
    try:
        await client.start(token)
    except discord.errors.PrivilegedIntentsRequired:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⚠️  INTENTS NÃO ATIVADOS!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\nO bot tentou conectar mas você ainda não ativou os intents.")
        print("\nMAS consegui verificar: O bot está CONFIGURADO corretamente!")
        print("Só precisa ativar os intents para funcionar.\n")
        print("Veja: ATIVAR_INTENTS.txt")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    except discord.errors.LoginFailure:
        print("\n❌ Token inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(verificar_servidores())
