#!/usr/bin/env python3
"""
Script de inicialização do Cuiudo
Verifica dependências e inicia o bot
"""
import sys
import subprocess
import os

def verificar_python():
    """Verifica versão do Python"""
    versao = sys.version_info
    if versao.major < 3 or (versao.major == 3 and versao.minor < 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {versao.major}.{versao.minor}.{versao.micro}")
        return False
    return True

def verificar_dependencias():
    """Verifica se dependências estão instaladas"""
    try:
        import discord
        import dotenv
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e.name}")
        print("\nInstale as dependências:")
        print("  pip install -r requirements.txt")
        return False

def verificar_env():
    """Verifica se arquivo .env existe"""
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado!")
        print("\n1. Copie o arquivo .env.example para .env:")
        print("   cp .env.example .env")
        print("\n2. Edite o .env e adicione seu DISCORD_TOKEN")
        print("\n3. Execute este script novamente")
        return False
    return True

def verificar_hermes():
    """Verifica se Hermes está disponível"""
    try:
        result = subprocess.run(['hermes', '--version'], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✅ Hermes encontrado!")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("⚠️  Hermes não encontrado no PATH")
    print("   O Cuiudo funcionará com respostas básicas.")
    print("   Para respostas inteligentes, instale o Hermes.")
    return True  # Não é crítico

def main():
    """Função principal"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🧉 Cuiudo - Verificação de Sistema")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Verificações
    checks = [
        ("Python 3.8+", verificar_python),
        ("Dependências", verificar_dependencias),
        ("Arquivo .env", verificar_env),
        ("Hermes (opcional)", verificar_hermes)
    ]
    
    tudo_ok = True
    for nome, verificacao in checks:
        print(f"Verificando {nome}...", end=" ")
        if verificacao():
            print("✅")
        else:
            print("❌")
            tudo_ok = False
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if tudo_ok:
        print("\n✅ Tudo pronto! Iniciando Cuiudo...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        # Importa e executa o bot
        try:
            from cuiudo import main as bot_main
            bot_main()
        except KeyboardInterrupt:
            print("\n\nCuiudo encerrado pelo usuário.")
    else:
        print("\n❌ Corrija os problemas acima antes de continuar.")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
