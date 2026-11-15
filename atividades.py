"""
Atividades rotativas do Cuiudo
Simulam a vida diária de um colono gaúcho
"""
import random
from datetime import datetime

class AtividadesGauchas:
    """Sistema de atividades que simulam a rotina de um gaúcho"""
    
    # Atividades por período do dia
    ATIVIDADES = {
        'manha': [
            '☀️ Cevando um mate',
            '🌄 Cuidando da criação',
            '🐴 Na lida campeira',
            '☕ Tomando café colonial',
            '🌾 Olhando a lavoura',
            '🧉 Preparando o mate',
            '🐔 Cuidando das galinhas'
        ],
        'tarde': [
            '🧉 Cevando uns mates',
            '🥩 Pensando no churrasco',
            '🎵 Ouvindo música gauchesca',
            '📻 Escutando o rádio',
            '🌳 Descansando no galpão',
            '🐴 Domando um bagual',
            '🔥 Preparando a lenha'
        ],
        'noite': [
            '🌙 Cevando um mate',
            '🔥 Ao redor do fogo',
            '🎸 Tocando violão',
            '🍖 Fazendo um assado',
            '🌟 Olhando as estrelas',
            '🎵 Cantando uma trova',
            '💬 Contando causos'
        ],
        'madrugada': [
            '😴 Dormindo no galpão',
            '🌙 Descansando',
            '💤 Sonhando com churrasco',
            '🛌 Na cama',
            '🦉 Noite tranquila'
        ]
    }
    
    # Atividades especiais (ocasionais)
    ATIVIDADES_ESPECIAIS = [
        '🎉 Preparando um fandango',
        '🏇 Nos Jogos Campeiros',
        '🎪 Na Semana Farroupilha',
        '🥩 Carneando para o churrasco',
        '🌾 Colhendo bergamota',
        '🐴 Treinando crioulo',
        '🎯 Jogando tava',
        '🎸 Ensaiando com os gaudérios',
        '⚽ Jogando bocha',
        '🧉 No rodeio de mate',
        '📖 Lendo o Martim Fierro',
        '🎭 Nos Festejos Farroupilhas'
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
        Combinação de atividade com frase gaúcha
        """
        frases = [
            'Vida boa tchê!',
            'Bah, que dia!',
            'Tri legal!',
            'Barbaridade!',
            'Na paz tchê',
            'Vida campeira',
            'É nóis!',
            'Firme e forte!'
        ]
        
        # 20% de chance de adicionar uma frase
        if random.random() < 0.20:
            return f"{AtividadesGauchas.pegar_atividade()} - {random.choice(frases)}"
        
        return AtividadesGauchas.pegar_atividade()
