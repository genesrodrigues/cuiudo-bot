"""
Sistema de Respostas Contextuais do Bastião
Gera respostas naturais sem depender de LLM externo
Baseado em padrões, contexto e personalidade gaúcha
"""
import random
import re

class GeradorRespostas:
    """Gera respostas contextuais para o Bastião"""
    
    # Padrões de conversa e respostas
    PADROES = {
        # Convites e propostas
        'convite': {
            'padroes': [
                r'(quer|vamos|bora|vem).*(ir|vir|fazer|tomar|comer)',
                r'(bodega|bar|churrasco|mate|chimarrão)',
                r'vamo.*(pro|pra|na)',
            ],
            'respostas': [
                "Bah guri, boa ideia! Tô dentro tchê! {entusiasmo}",
                "Claro que sim! {aprovacao} Vamo nessa!",
                "Barbaridade, pode contar comigo! {aprovacao}",
                "Bah, com 70 anos não perco uma boa prosa! Bora!",
                "Opa, aceito sim tchê! {aprovacao}"
            ],
            'complementos': {
                'entusiasmo': ['Bah, que tri!', 'Vai ser bom!', 'Tava querendo sair mesmo!'],
                'aprovacao': ['Muito bom!', 'Baita ideia!', 'Isso sim!']
            }
        },
        
        # Perguntas sobre ele
        'sobre_mim': {
            'padroes': [
                r'(quantos anos|idade|velho|idoso)',
                r'(onde mora|de onde|cidade)',
                r'(o que faz|trabalha|profissão)',
                r'(casado|família|esposa|filhos)',
            ],
            'respostas_idade': [
                "Bah, já tenho 70 anos tchê! Muita estrada percorrida...",
                "Tenho 70 anos de idade e muita história pra contar!",
                "Bah guri, 70 anos nas costas! Já vi muita coisa nessa vida.",
                "Setenta anos de vida, guri. Sou dos antigos!"
            ],
            'respostas_origem': [
                "Sou gaúcho de raiz tchê! Nasci e me criei no campo.",
                "Do Rio Grande do Sul, guri! Campeiro de verdade.",
                "Bah, sou gaúcho legítimo! 70 anos de querência!",
                "Do campo gaúcho, tchê! Vida toda aqui nos pampas."
            ],
            'respostas_trabalho': [
                "Trabalhei a vida toda na lida campeira, guri. Hoje tô mais sossegado.",
                "Fui campeiro a vida inteira! Agora tô nos tempos de descanso.",
                "Bah, 50 anos na lida do campo! Agora só cevo mate e conto causo.",
                "Fui peão, campeiro, de tudo um pouco. Vida no campo tchê!"
            ],
            'respostas_familia': [
                "Tenho família boa, guri! Esposa, filhos, netos... Vida abençoada!",
                "Sou casado há muitos anos tchê! Família grande e unida.",
                "Bah, família é tudo! Tenho esposa, filhos e uns quantos netos!",
                "Família grande e tradicionalista, guri! Orgulho meu!"
            ]
        },
        
        # Saudações
        'saudacao': {
            'padroes': [
                r'^(oi|olá|opa|e aí|salve|bom dia|boa tarde|boa noite)',
                r'(como vai|como está|tudo bem|beleza)',
            ],
            'respostas': [
                "Bah, como vai guri? Tô bem tchê! E tu?",
                "Opa! Tudo certo por aqui! Cevando um mate. E contigo?",
                "Bah, tô firme e forte! {complemento} E tu, como anda?",
                "Salve! Tô na paz, descansando. {complemento}",
                "E aí tchê! Tô bem sim! {complemento}"
            ],
            'complementos': [
                'Mais um dia de vida!',
                '70 anos mas tô ativo!',
                'Idade chegando mas tô bem!',
                'Sempre firme tchê!'
            ]
        },
        
        # Humor e clima
        'humor_clima': {
            'padroes': [
                r'(frio|calor|chuva|sol|tempo|clima)',
                r'(tá (quente|frio|chovendo))',
            ],
            'respostas_frio': [
                "Bah, tá um frio brabo mesmo! Mas já vi piores nesses 70 anos...",
                "Minuano tá puxado tchê! Bom pra ficar em casa cevando mate.",
                "Bah, que frio! Mas nós gaúcho aguenta bem!",
                "Esse vento sul tá de lascar! Mas já acostumei ao longo dos anos."
            ],
            'respostas_calor': [
                "Bah, calor brabo! Bom pra tomar um mate gelado na sombra.",
                "Tá quente demais tchê! Nos meus tempos era mais fresco...",
                "Barbaridade de calor! Vou ficar na sombra aqui."
            ],
            'respostas_chuva': [
                "Tá chovendo bem! Bom pra terra, guri.",
                "Bah, chuvarada boa! Lembra os temporais de antigamente.",
                "Chuva tchê! Bom ficar em casa cevando mate."
            ]
        },
        
        # Comida e bebida
        'comida_bebida': {
            'padroes': [
                r'(fome|comer|comida|almoço|janta)',
                r'(sede|beber|bebida|tomar)',
                r'(mate|chimarrão|churrasco|café)',
            ],
            'respostas_mate': [
                "Bah, tô sempre cevando um mate tchê! Quer um?",
                "Mate nunca falta aqui! Tomo o dia inteiro.",
                "Chimarrão é sagrado, guri! Já cevei uns quantos hoje.",
                "Mate bem amargo, do jeito que aprendi com meu pai!"
            ],
            'respostas_churrasco': [
                "Bah, churrasco é sempre bom! Faço desde guri, mais de 50 anos!",
                "Churrasco no fogo de chão, sal grosso... Isso sim é coisa boa!",
                "Barbaridade, faz tempo que não faço um assado! Boas lembranças.",
                "Churrasco é arte, guri! Aprendi com os antigos."
            ],
            'respostas_comida': [
                "Bah, comida boa é comida caseira tchê! Do jeito antigo.",
                "Café colonial, pão caseiro, chimia... Isso sim!",
                "Comida campeira é a melhor! Carreteiro, arroz de carreteiro...",
                "Tô sempre bem alimentado! Comida boa não falta."
            ]
        },
        
        # Sentimentos e estados
        'sentimentos': {
            'padroes': [
                r'(cansado|sono|dormir)',
                r'(feliz|alegre|contente)',
                r'(triste|chateado|mal)',
                r'(saudade|lembranças)',
            ],
            'respostas_cansaco': [
                "Bah, com 70 anos o cansaço chega mais rápido tchê!",
                "Tô um pouco cansado sim, mas é a idade!",
                "Cansaço da idade, guri. Mas tô bem!"
            ],
            'respostas_feliz': [
                "Tô bem feliz sim tchê! Vida boa, família bem...",
                "Bah, contentamento! Gratidão pela vida!",
                "Feliz e agradecido, guri! 70 anos de muita bênção!"
            ],
            'respostas_saudade': [
                "Bah, saudades dos tempos antigos... Mas foram bons tempos!",
                "Tenho saudade sim, guri. Dos velhos amigos, da lida no campo...",
                "Saudades de quando era mais novo, tchê. Mas a vida segue!",
                "Muita saudade dos antigos... Mas as lembranças são boas!"
            ]
        },
        
        # Genérico positivo
        'generico_positivo': {
            'padroes': [
                r'(bom|legal|bacana|massa|tri)',
                r'(gostei|adorei|curti)',
            ],
            'respostas': [
                "Bah, que bom tchê! {aprovacao}",
                "Isso sim é que é! {aprovacao}",
                "Barbaridade de bom! {aprovacao}",
                "Baita coisa boa! {aprovacao}",
                "Muito bom mesmo tchê! {aprovacao}"
            ],
            'aprovacao': ['Fico feliz!', 'Que alegria!', 'Bah, tri!']
        },
        
        # Despedidas
        'despedida': {
            'padroes': [
                r'(tchau|até logo|até mais|falou|abraço|até)',
                r'(vou (embora|indo|sair|nessa))',
            ],
            'respostas': [
                "Até logo tchê! Fica com Deus!",
                "Tchau guri! A gente se vê!",
                "Abraço tchê! Até a próxima!",
                "Até mais! Que Deus te acompanhe!",
                "Falou guri! Se cuida tchê!"
            ]
        }
    }
    
    @staticmethod
    def gerar_resposta(mensagem, usuario=None):
        """
        Gera resposta contextual baseada na mensagem
        
        Returns:
            (resposta: str, confianca: float)
        """
        mensagem_lower = mensagem.lower()
        
        # Tenta cada categoria de padrão
        for categoria, config in GeradorRespostas.PADROES.items():
            # Verifica padrões
            padroes = config.get('padroes', [])
            for padrao in padroes:
                if re.search(padrao, mensagem_lower):
                    # Achou padrão! Gera resposta
                    resposta = GeradorRespostas._gerar_resposta_categoria(
                        categoria, config, mensagem_lower, usuario
                    )
                    
                    # Se retornou None, continua tentando outros padrões
                    if resposta:
                        return resposta, 0.8
        
        # Nenhum padrão encontrado - resposta genérica contextual
        return GeradorRespostas._resposta_generica_contextual(mensagem, usuario), 0.3
    
    @staticmethod
    def _gerar_resposta_categoria(categoria, config, mensagem, usuario):
        """Gera resposta específica da categoria"""
        
        # Casos especiais por categoria
        if categoria == 'sobre_mim':
            if 'idade' in mensagem or 'anos' in mensagem or 'velho' in mensagem:
                return random.choice(config['respostas_idade'])
            elif 'mora' in mensagem or 'onde' in mensagem or 'cidade' in mensagem:
                return random.choice(config['respostas_origem'])
            elif 'trabalha' in mensagem or 'faz' in mensagem or 'profissão' in mensagem:
                return random.choice(config['respostas_trabalho'])
            elif 'família' in mensagem or 'casado' in mensagem or 'filhos' in mensagem:
                return random.choice(config['respostas_familia'])
        
        elif categoria == 'humor_clima':
            if 'frio' in mensagem:
                return random.choice(config['respostas_frio'])
            elif 'calor' in mensagem or 'quente' in mensagem:
                return random.choice(config['respostas_calor'])
            elif 'chuva' in mensagem or 'chovendo' in mensagem:
                return random.choice(config['respostas_chuva'])
        
        elif categoria == 'comida_bebida':
            if 'mate' in mensagem or 'chimarrão' in mensagem:
                return random.choice(config['respostas_mate'])
            elif 'churrasco' in mensagem:
                return random.choice(config['respostas_churrasco'])
            else:
                return random.choice(config['respostas_comida'])
        
        elif categoria == 'sentimentos':
            if 'cansado' in mensagem or 'sono' in mensagem:
                return random.choice(config['respostas_cansaco'])
            elif 'feliz' in mensagem or 'alegre' in mensagem:
                return random.choice(config['respostas_feliz'])
            elif 'saudade' in mensagem:
                return random.choice(config['respostas_saudade'])
        
        # Respostas padrão da categoria
        respostas = config.get('respostas', [])
        if respostas:
            resposta = random.choice(respostas)
            
            # Substitui placeholders
            complementos = config.get('complementos', {})
            
            # Verifica se complementos é dict ou list
            if isinstance(complementos, dict):
                for key, valores in complementos.items():
                    placeholder = '{' + key + '}'
                    if placeholder in resposta:
                        resposta = resposta.replace(placeholder, random.choice(valores))
            elif isinstance(complementos, list):
                # Se for lista, substitui qualquer {placeholder}
                if '{' in resposta:
                    resposta = resposta.replace('{complemento}', random.choice(complementos))
            
            # Remove placeholders não substituídos
            resposta = re.sub(r'\{[^}]+\}', '', resposta).strip()
            
            return resposta
        
        return None
    
    @staticmethod
    def _resposta_generica_contextual(mensagem, usuario):
        """Gera resposta genérica mas contextual"""
        
        # Extrai palavras-chave da mensagem
        palavras = mensagem.lower().split()
        
        # Respostas genéricas com tom de veterano
        templates = [
            "Bah guri, sobre {assunto}... Deixa eu pensar tchê.",
            "Opa, {assunto}? Bah, é uma boa pergunta!",
            "Bah, sobre {assunto} posso te dizer que...",
            "Barbaridade, {assunto}! Isso me lembra dos tempos antigos.",
            "Bah guri, {assunto}... Com 70 anos já vi de tudo!",
        ]
        
        # Respostas quando não entende bem
        respostas_nao_entendeu = [
            "Bah guri, não entendi muito bem... Pode explicar melhor tchê?",
            "Opa, me perdi aqui! Como é que é?",
            "Barbaridade, tô meio confuso! Explica de novo?",
            "Bah, com 70 anos às vezes a gente se perde... O que tu disse?",
            "Capaz, não peguei bem tchê! Repete aí?",
            "Bah guri, tô meio aéreo hoje! Me explica melhor?"
        ]
        
        # Se mensagem muito curta, diz que não entendeu
        if len(palavras) <= 2:
            return random.choice(respostas_nao_entendeu)
        
        # Tenta extrair assunto
        substantivos_comuns = ['coisa', 'jeito', 'vez', 'dia', 'tempo', 'gente']
        palavras_interessantes = [p for p in palavras if len(p) > 3 and p not in substantivos_comuns]
        
        if palavras_interessantes:
            assunto = random.choice(palavras_interessantes)
            template = random.choice(templates)
            
            # Complemento
            complementos = [
                "Me conta mais sobre isso!",
                "Bah, interessante tchê!",
                "Conta mais, guri!",
                "Bah, quero saber mais!",
            ]
            
            return f"{template.replace('{assunto}', assunto)} {random.choice(complementos)}"
        
        return random.choice(respostas_nao_entendeu)
