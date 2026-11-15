# Comando para ver quantos aprendizados o Bastião tem
# Execute: python ver_aprendizados.py

from memoria_aprendizado import MemoriaBastiao

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📚 MEMÓRIA DO BASTIÃO")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    memoria = MemoriaBastiao()
    
    total = memoria.contar_aprendizados()
    print(f"Total de aprendizados: {total}")
    print(f"Tópicos conhecidos: {len(memoria.memoria['topicos'])}")
    print(f"Pessoas conhecidas: {len(memoria.memoria['pessoas'])}")
    
    if total > 0:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("ÚLTIMOS 5 APRENDIZADOS:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        for apr in memoria.ultimos_aprendizados(5):
            print(f"📌 {apr['topico']}")
            print(f"   {apr['informacao'][:100]}...")
            print(f"   Fonte: {apr['fonte']} ({apr['data'][:10]})\n")
    else:
        print("\n⚠️  Bastião ainda não aprendeu nada!")
        print("   Teste perguntando: '@Bastião o que é chimarrão?'")
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

if __name__ == "__main__":
    main()
