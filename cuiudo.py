"""
Cuiudo - Assistente Discord Gaúcho
Bot Discord com personalidade autêntica de gaúcho do Rio Grande do Sul
Processamento local via Hermes
"""
import discord
from discord.ext import commands, tasks
import asyncio
import random
from datetime import datetime

# Importa módulos do Cuiudo
import config
from personalidade import PersonalidadeGaucha
from atividades import AtividadesGauchas
from hermes_integration import HermesIntegration

class Cuiudo(commands.Bot):
    """Bot Discord com personalidade gaúcha"""
    
    def __init__(self):
        # Configuração de intents (permissões)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        
        super().__init__(
            command_prefix=config.COMMAND_PREFIX,
            intents=intents,
            help_command=None  # Removemos o comando help padrão
        )
        
        # Sistemas do Cuiudo
        self.personalidade = PersonalidadeGaucha()
        self.atividades = AtividadesGauchas()
        self.hermes = HermesIntegration(verbose=config.VERBOSE)
        
        # Estado
        self.iniciado = False
        self.ultima_atividade = None
    
    async def setup_hook(self):
        """Inicialização assíncrona"""
        # Inicia task de rotação de atividades
        self.rotacionar_atividade.start()
        
        if config.VERBOSE:
            print("Cuiudo inicializado!")
    
    async def on_ready(self):
        """Evento: bot conectado ao Discord"""
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🧉 Cuiudo conectado com sucesso!")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Nome: {self.user.name}")
        print(f"   ID: {self.user.id}")
        print(f"   Servidores: {len(self.guilds)}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Bah tchê! Tô online e pronto pra prosa!")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        # Define primeira atividade
        await self._atualizar_atividade()
        self.iniciado = True
    
    async def on_member_join(self, member):
        """Evento: novo membro entra no servidor"""
        # Busca canal de boas-vindas
        canal = discord.utils.get(member.guild.text_channels, name=config.WELCOME_CHANNEL_NAME)
        
        if canal:
            # Mensagem de boas-vindas personalizada
            mensagem = self.personalidade.mensagem_boas_vindas(member.mention)
            
            # Adiciona uma dica sobre chimarrão ou churrasco (20% de chance)
            if random.random() < 0.20:
                dicas = [
                    "\nBah, se quiser tomar um mate, tô sempre cevando!",
                    "\nAqui a gente é tri receptivo, pode ficar tranquilo!",
                    "\nBem-vindo à nossa querência, se sinta em casa!",
                    "\nChega mais e puxa uma cadeira pra prosa!",
                    "\nQualquer coisa é só chamar, tamo junto tchê!"
                ]
                mensagem += random.choice(dicas)
            
            await canal.send(mensagem)
            
            if config.VERBOSE:
                print(f"Boas-vindas enviadas para {member.name}")
    
    async def on_message(self, message):
        """Evento: mensagem enviada em algum canal"""
        # Ignora mensagens do próprio bot
        if message.author == self.user:
            return
        
        # Ignora mensagens de outros bots
        if message.author.bot:
            return
        
        # Verifica se o bot foi mencionado
        foi_mencionado = self.user.mentioned_in(message)
        
        # Verifica se é uma mensagem direta
        eh_dm = isinstance(message.channel, discord.DMChannel)
        
        # Responde se foi mencionado ou é DM
        if foi_mencionado or eh_dm:
            await self._responder_mensagem(message)
        
        # Processa comandos (se houver)
        await self.process_commands(message)
    
    async def _responder_mensagem(self, message):
        """Processa e responde uma mensagem"""
        # Mostra que está digitando
        async with message.channel.typing():
            # Remove menção do bot da mensagem
            conteudo = message.content
            if self.user.mentioned_in(message):
                conteudo = conteudo.replace(f'<@{self.user.id}>', '').strip()
                conteudo = conteudo.replace(f'<@!{self.user.id}>', '').strip()
            
            if not conteudo:
                conteudo = "Oi!"
            
            # Processa com Hermes
            nome_usuario = message.author.display_name
            resposta = await self.hermes.processar_mensagem_async(conteudo, usuario=nome_usuario)
            
            # Envia resposta
            await message.reply(resposta, mention_author=False)
            
            if config.VERBOSE:
                print(f"[{nome_usuario}]: {conteudo}")
                print(f"[Cuiudo]: {resposta}")
    
    @tasks.loop(seconds=config.ACTIVITY_INTERVAL)
    async def rotacionar_atividade(self):
        """Task: rotaciona atividade do bot periodicamente"""
        if self.iniciado:
            await self._atualizar_atividade()
    
    async def _atualizar_atividade(self):
        """Atualiza a atividade/status do bot"""
        atividade_texto = self.atividades.pegar_status_personalizado()
        
        # Evita repetir a mesma atividade
        if atividade_texto == self.ultima_atividade:
            atividade_texto = self.atividades.pegar_status_personalizado()
        
        self.ultima_atividade = atividade_texto
        
        # Define atividade no Discord
        # Tipos: playing, listening, watching, competing
        tipos_atividade = [
            discord.ActivityType.playing,
            discord.ActivityType.watching,
            discord.ActivityType.listening
        ]
        
        tipo = random.choice(tipos_atividade)
        atividade = discord.Activity(type=tipo, name=atividade_texto)
        
        await self.change_presence(activity=atividade, status=discord.Status.online)
        
        if config.VERBOSE:
            print(f"Atividade atualizada: {atividade_texto}")
    
    # ===== COMANDOS =====
    
    @commands.command(name='mate', aliases=['chimarrão', 'chimarrao'])
    async def comando_mate(self, ctx):
        """Comando: fala sobre chimarrão"""
        resposta = self.personalidade.pegar_tema('chimarrao')
        await ctx.send(resposta)
    
    @commands.command(name='churrasco')
    async def comando_churrasco(self, ctx):
        """Comando: fala sobre churrasco"""
        resposta = self.personalidade.pegar_tema('churrasco')
        await ctx.send(resposta)
    
    @commands.command(name='giria', aliases=['gíria'])
    async def comando_giria(self, ctx):
        """Comando: ensina uma gíria gaúcha"""
        categoria = random.choice(list(self.personalidade.GIRIAS.keys()))
        giria = self.personalidade.pegar_giria(categoria)
        
        explicacoes = {
            'cumprimento': 'é como a gente se cumprimenta',
            'surpresa': 'é pra quando tu fica surpreso',
            'aprovacao': 'é quando algo tá tri bom',
            'concordancia': 'é pra concordar com alguém',
            'negacao': 'é pra negar algo com surpresa',
            'despedida': 'é como a gente se despede'
        }
        
        explicacao = explicacoes.get(categoria, 'é uma expressão gaúcha')
        
        await ctx.send(f"{giria} - {explicacao} tchê!")
    
    @commands.command(name='ajuda', aliases=['help', 'comandos'])
    async def comando_ajuda(self, ctx):
        """Comando: mostra ajuda"""
        ajuda = """🧉 **Cuiudo - Comandos**

**Conversar:**
- Me mencione ou mande mensagem direta pra trocar ideia!

**Comandos:**
- `!mate` ou `!chimarrão` - Falo sobre mate
- `!churrasco` - Falo sobre churrasco  
- `!giria` - Te ensino uma gíria gaúcha
- `!ajuda` - Mostra esta mensagem

**Sobre mim:**
Sou o Cuiudo, um gaúcho legítimo que adora uma boa prosa!
Bah tchê, pode falar comigo sobre mate, churrasco, campo, tradições...

Chega mais e vamos trocar ideia! 🤠
"""
        await ctx.send(ajuda)
    
    @commands.command(name='ping')
    async def comando_ping(self, ctx):
        """Comando: teste de latência"""
        latencia = round(self.latency * 1000)
        await ctx.send(f"Bah, tô ligeiro! Latência: {latencia}ms tchê!")

def main():
    """Função principal"""
    # Verifica se o token foi configurado
    if not config.DISCORD_TOKEN:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("❌ ERRO: Token do Discord não configurado!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\nPor favor:")
        print("1. Crie um arquivo .env na raiz do projeto")
        print("2. Adicione: DISCORD_TOKEN=seu_token_aqui")
        print("\nVeja .env.example para referência")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        return
    
    # Cria e executa o bot
    bot = Cuiudo()
    
    try:
        bot.run(config.DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("❌ ERRO: Token do Discord inválido!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\nVerifique se o token no arquivo .env está correto.")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    except KeyboardInterrupt:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🧉 Cuiudo desconectado!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Até logo tchê!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

if __name__ == "__main__":
    main()
