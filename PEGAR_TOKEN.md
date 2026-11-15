# Como Pegar o Token do Bot Discord

Você tem o Application ID e Client Secret, mas precisa do **BOT TOKEN**. São coisas diferentes!

## Passos:

### 1. Acesse a página do Bot

Use este link direto (já com seu Application ID):
```
https://discord.com/developers/applications/1571489070952095744/bot
```

Ou manualmente:
1. Vá em https://discord.com/developers/applications
2. Clique na aplicação **Cuiudo** (ou o nome que você deu)
3. No menu lateral, clique em **"Bot"**

### 2. Ativar Intents (IMPORTANTE!)

Role a página e encontre **"Privileged Gateway Intents"**:

- ✅ **PRESENCE INTENT**
- ✅ **SERVER MEMBERS INTENT**  
- ✅ **MESSAGE CONTENT INTENT** ← **ESSENCIAL!**

Clique **"Save Changes"** se aparecer.

### 3. Copiar o Token

Na seção **"TOKEN"** (topo da página):

- Se é primeira vez: clique **"Reset Token"**
- Se já gerou antes: clique **"Copy"**

⚠️ **O token aparece apenas UMA VEZ!** Copie e guarde bem!

Exemplo de como o token parece:
```
MTU3MTQ4OTA3MDk1MjA5NTc0NA.GxYzAB.dQw4w9WgXcQ-abc123xyz789...
```

### 4. Colar no .env

1. Abra o arquivo `.env` no projeto
2. Encontre a linha:
   ```
   DISCORD_TOKEN=COLE_O_TOKEN_DO_BOT_AQUI
   ```
3. Substitua por:
   ```
   DISCORD_TOKEN=seu_token_completo_aqui
   ```
4. Salve o arquivo

### 5. Adicionar o Bot ao Servidor

Se ainda não adicionou:

1. Vá em **OAuth2** > **URL Generator**
2. Selecione:
   - Scopes: ✅ `bot`
   - Permissions: ✅ Send Messages, ✅ Read Messages, ✅ Embed Links
3. Copie a URL gerada
4. Cole no navegador e autorize no seu servidor

### 6. Testar!

```bash
python iniciar.py
```

Deve aparecer:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧉 Cuiudo conectado com sucesso!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Diferenças:

| O que você enviou | Para que serve |
|-------------------|----------------|
| Application ID | Identificar a aplicação |
| Public Key | Verificação de interações |
| Client Secret | OAuth2 (login com Discord) |
| **BOT TOKEN** ← | **Autenticar o bot** ✅ |

---

**Bah tchê, quando pegar o token é só colar no .env e rodar!** 🧉
