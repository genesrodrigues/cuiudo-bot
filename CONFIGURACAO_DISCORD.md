# Configuração Discord - Passo a Passo

## 1. Criar Aplicação no Discord

1. Acesse https://discord.com/developers/applications
2. Clique em **"New Application"**
3. Nome: **Cuiudo** (ou outro nome de sua escolha)
4. Aceite os termos e clique **"Create"**

## 2. Configurar o Bot

1. No menu lateral, clique em **"Bot"**
2. Clique em **"Add Bot"**
3. Confirme clicando **"Yes, do it!"**

### Configurações Importantes:

**PUBLIC BOT:**
- ☑️ Ativado (se quiser que outros possam adicionar)
- ⬜ Desativado (se quiser apenas no seu servidor)

**REQUIRES OAUTH2 CODE GRANT:**
- ⬜ Deixe desativado

## 3. Permissões (Intents)

No mesmo menu **"Bot"**, role até **Privileged Gateway Intents**:

- ✅ **PRESENCE INTENT** (para ver status de usuários)
- ✅ **SERVER MEMBERS INTENT** (para boas-vindas)
- ✅ **MESSAGE CONTENT INTENT** (para ler mensagens) **← IMPORTANTE!**

Clique **"Save Changes"** se aparecer.

## 4. Copiar o Token

1. No topo da página, seção **"TOKEN"**
2. Clique em **"Reset Token"** (primeira vez) ou **"Copy"**
3. **⚠️ IMPORTANTE:** Guarde este token em local seguro!
4. **NUNCA** compartilhe ou commite este token

## 5. Configurar .env

1. No projeto, copie `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env`:
   ```env
   DISCORD_TOKEN=cole_seu_token_aqui
   ```

3. Salve o arquivo

## 6. Gerar Link de Convite

1. No menu lateral, clique em **"OAuth2"**
2. Clique em **"URL Generator"**

**Scopes (selecione):**
- ✅ `bot`

**Bot Permissions (selecione):**
- ✅ Read Messages/View Channels
- ✅ Send Messages
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Add Reactions
- ✅ Use Slash Commands (opcional)

3. Copie a URL gerada no final da página

## 7. Adicionar ao Servidor

1. Cole a URL copiada no navegador
2. Selecione o servidor onde quer adicionar o bot
3. Clique **"Autorizar"**
4. Complete o CAPTCHA
5. Pronto! O bot aparecerá offline no servidor

## 8. Iniciar o Bot

```bash
# Instale dependências primeiro (se não fez)
pip install -r requirements.txt

# Execute o bot
python iniciar.py
```

Ou diretamente:
```bash
python cuiudo.py
```

## 9. Verificar Funcionamento

No Discord:
1. Veja se o bot aparece **ONLINE** na lista de membros
2. Teste com: `@Cuiudo oi`
3. Teste comandos: `!mate`, `!ajuda`

## Troubleshooting

### Bot não conecta
- ✅ Verifique se o token está correto no `.env`
- ✅ Verifique se não há espaços extras no token
- ✅ Certifique-se que Message Content Intent está ativado

### Bot não responde
- ✅ Verifique se Message Content Intent está ativado
- ✅ Teste mencionando o bot: `@Cuiudo`
- ✅ Verifique logs no terminal

### Erro de permissões
- ✅ Verifique se o bot tem permissão para enviar mensagens no canal
- ✅ Reenvie o convite com permissões corretas
- ✅ Verifique hierarquia de cargos no servidor

### Hermes não encontrado
- ✅ Instale Hermes: https://hermes-agent.nousresearch.com
- ✅ Adicione Hermes ao PATH do sistema
- ✅ Bot funciona sem Hermes (respostas básicas)

## Configurações Adicionais

### Alterar Canal de Boas-vindas

Edite `config.py`:
```python
WELCOME_CHANNEL_NAME = 'geral'  # Nome do seu canal
```

### Alterar Intervalo de Atividades

No `.env`:
```env
CUIUDO_ACTIVITY_INTERVAL=300  # Segundos (300 = 5min)
```

### Ativar Logs Detalhados

No `.env`:
```env
CUIUDO_VERBOSE=true
```

## Recursos do Bot

✅ Boas-vindas automáticas  
✅ Responde quando mencionado  
✅ Responde em mensagens diretas  
✅ Comandos (!mate, !churrasco, etc)  
✅ Atividades rotativas  
✅ Personalidade gaúcha autêntica  
✅ Integração com Hermes (opcional)  
✅ Filtros de segurança  

---

**Pronto tchê! Bah, agora é só aproveitar!** 🧉

## Links Úteis

- Discord Developer Portal: https://discord.com/developers/applications
- Discord.py Docs: https://discordpy.readthedocs.io/
- Hermes: https://hermes-agent.nousresearch.com/
