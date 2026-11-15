# Cuiudo - Assistente Discord Gaúcho 🧉

Bah tchê! O Cuiudo é um assistente Discord com personalidade autêntica de gaúcho, rodando 100% local usando Hermes.

## Sobre o Cuiudo

O Cuiudo é um colono gaúcho que vive no seu servidor Discord. Ele dá boas-vindas, conversa usando gírias gauchescas autênticas, e tem suas próprias atividades que dão a impressão de ser uma pessoa real.

**Características:**
- 🧉 Personalidade gaúcha autêntica com gírias regionais
- 🤝 Boas-vindas calorosas para novos membros
- 💬 Conversa natural usando Hermes localmente
- 🔒 Sem acesso a comandos do sistema (seguro)
- 🎭 Atividades rotativas simulando vida de colono
- 🏠 Roda 100% na sua máquina

## Requisitos

- Python 3.8+
- Hermes instalado e configurado
- Conta Discord e permissões para criar bot

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repo>
cd cuiudo-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as credenciais do Discord:

Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_TOKEN=seu_token_aqui
DISCORD_GUILD_ID=id_do_servidor (opcional)
```

4. Execute o bot:
```bash
python cuiudo.py
```

## Configurando o Bot Discord

1. Acesse https://discord.com/developers/applications
2. Clique em "New Application"
3. Dê um nome (Cuiudo)
4. Vá em "Bot" no menu lateral
5. Clique em "Add Bot"
6. Copie o TOKEN e cole no arquivo `.env`
7. Ative as "Privileged Gateway Intents":
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

8. Vá em "OAuth2" > "URL Generator"
9. Selecione:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Read Messages`, `Manage Messages`, `Embed Links`
10. Copie a URL gerada e abra no navegador para adicionar ao servidor

## Personalidade do Cuiudo

O Cuiudo é um gaúcho autêntico que:
- Usa gírias como "bah", "tchê", "tri", "barbaridade"
- Fala sobre chimarrão, churrasco, vida no campo
- Tem atividades como "Cevando um mate", "Na lida campeira", "Carneando"
- É hospitaleiro e receptivo com novos membros
- Não fornece informações técnicas do sistema
- Mantém conversas casuais e amigáveis

## Estrutura do Projeto

```
cuiudo-bot/
├── cuiudo.py              # Bot principal
├── personalidade.py       # Sistema de personalidade gaúcha
├── hermes_integration.py  # Integração com Hermes
├── atividades.py          # Atividades rotativas
├── config.py              # Configurações
├── .env                   # Credenciais (NÃO commitar!)
├── .gitignore
├── requirements.txt
└── README.md
```

## Segurança

- O Cuiudo NÃO executa comandos do sistema
- NÃO fornece informações técnicas da máquina
- Todas as respostas passam por filtro de segurança
- Roda isolado via Hermes em modo restrito

## Contribuindo

Sugestões de novas gírias, atividades ou melhorias na personalidade são bem-vindas!

## Licença

MIT

---

**Bah, tri legal esse projeto tchê!** 🧉
