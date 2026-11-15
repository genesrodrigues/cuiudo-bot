"""
Atividades rotativas do Bastião
Simulam a vida diária de um gaúcho de 70 anos
"""
import random
from datetime import datetime

class AtividadesGauchas:
    """Sistema de atividades que simulam a rotina de um gaúcho veterano (70 anos)"""
    
    # Atividades por período do dia (senhor de 70 anos)
    ATIVIDADES = {
        'manha': [
            '☀️ Cevando mate no galpão',
            '🌄 Olhando a criação',
            '☕ Tomando café colonial',
            '🧉 Preparando o chimarrão',
            '🪑 Descansando na varanda',
            '📻 Ouvindo rádio',
            '🌤️ Apreciando a manhã'
        ],
        'tarde': [
            '🧉 Cevando uns mates',
            '🥩 Lembrando dos churrascos antigos',
            '🎵 Ouvindo música gauchesca das antigas',
            '📻 Escutando o rádio',
            '🌳 Descansando no galpão',
            '🪑 Prosando na sombra',
            '📖 Lendo o jornal'
        ],
        'noite': [
            '🌙 Cevando mate na varanda',
            '🔥 Ao redor do fogo',
            '🎸 Ouvindo música das antigas',
            '📖 Contando causos',
            '🌟 Olhando as estrelas',
            '💬 Prosando com a família',
            '🪑 Descansando após o jantar'
        ],
        'madrugada': [
            '😴 Dormindo',
            '🌙 Descansando',
            '💤 Sonhando com os bons tempos',
            '🛌 Noite tranquila',
            '🦉 Sono profundo'
        ]
    }
    
    # Atividades especiais (ocasionais - senhor de 70 anos)
    ATIVIDADES_ESPECIAIS = [
        '📖 Relembrando histórias antigas',
        '🎪 Lembrando das Semanas Farroupilhas',
        '🥩 Orientando no churrasco',
        '🌾 Olhando a lavoura crescer',
        '🎸 Ouvindo música tradicionalista',
        '📻 No rodeio de mate',
        '🧉 Ensinando a cevar mate',
        '💬 Contando causos do passado',
        '🪑 Descansando na varanda',
        '🌤️ Apreciando o dia',
        '🤠 Lembrando dos tempos de peão',
        '📜 Recordando as tradições'
    ]
    
    @staticmethod
    def pegar_periodo_dia():
        """Determina o período do dia baseado na hora atual"""
        hora = datetime.now().hour
        
        if 5 <= hora < 12:
            return 'manha'
        elif 12 <= hora < 18:
            return 'tarde'
        elif 18 <= hora < 23:
            return 'noite'
        else:
            return 'madrugada'
    
    @staticmethod
    def pegar_atividade():
        """
        Retorna uma atividade apropriada para o período do dia
        10% de chance de ser uma atividade especial
        """
        if random.random() < 0.10:
            return random.choice(AtividadesGauchas.ATIVIDADES_ESPECIAIS)
        
        periodo = AtividadesGauchas.pegar_periodo_dia()
        atividades = AtividadesGauchas.ATIVIDADES.get(periodo, AtividadesGauchas.ATIVIDADES['tarde'])
        return random.choice(atividades)
    
    @staticmethod
    def pegar_status_personalizado():
        """
        Retorna uma mensagem de status personalizada
        Combinação de atividade com frase gaúcha (senhor de 70 anos)
        """
        frases = [
            'Bons tempos',
            'Vida calma',
            '70 anos de história',
            'Sempre firme',
            'Veterano gaúcho',
            'Memórias boas',
            'Tradição viva'
        ]
        
        # 20% de chance de adicionar uma frase
        if random.random() < 0.20:
            return f"{AtividadesGauchas.pegar_atividade()} - {random.choice(frases)}"
        
        return AtividadesGauchas.pegar_atividade()
