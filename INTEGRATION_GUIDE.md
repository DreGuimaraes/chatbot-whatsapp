# 📱 Integração WhatsApp

## ⚡ Instalação

```bash
# Instale as dependências
pip install -r requirements_whatsapp.txt

# Instale o pacote do sistema (se ainda não estiver)
pip install -e .
```

## 🚀 Uso Básico (WhatsApp Web)

### Passo 1: Inicialize o chatbot
```python
from whatsapp_integration import WhatsAppChatbot
from chatbot import LightweightChatbot

# Cria o chatbot (arquivo SQLite)
bot = LightweightChatbot("whatsapp_bot.db")

# Cria a integração WhatsApp
wa_bot = WhatsAppChatbot(bot)
```

### Passo 2: Inicie e escaneie o QR Code
```python
# Conecta ao WhatsApp Web
wa_bot.start()

# O QR code será exibido e salvo em qrcode_whatsapp.png
# Abra o WhatsApp no celular → Configurações → WhatsApp Web → Escaneie
```

### Passo 3: Use normalmente!
Após escanear, qualquer mensagem que você enviar no WhatsApp será respondida pelo chatbot.

## 🎯 Exemplo com Modelo Personalizado (OpenAI)

```python
import openai
from whatsapp_integration import WhatsAppChatbot
from chatbot import LightweightChatbot

# Configura sua chave OpenAI
openai.api_key = "sk-suachave"

# Função callback com o modelo
def chatgpt_model(history, user_input):
    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]
    messages.append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message.content

# Inicializa
bot = LightweightChatbot("whatsapp_openai.db")
wa_bot = WhatsAppChatbot(bot)

# Inicia com callback
wa_bot.start(model_callback=chatgpt_model)
```

## 🧪 Testando Localmente

```python
# Teste rápido sem modelo externo
from whatsapp_integration import WhatsAppChatbot
from chatbot import LightweightChatbot

bot = LightweightChatbot()
wa_bot = WhatsAppChatbot(bot)

print("Conectando...")
wa_bot.start()

# Envia mensagens pelo WhatsApp e veja as respostas
```

## 💾 Gerenciamento de Sessão

```python
# Salva a sessão para reconectar sem escanear novamente
wa_bot.save_session()

# Para encerrar limpamente
wa_bot.stop()
```

## 📂 Estrutura do Banco de Dados

O SQLite permanece o mesmo, mas com identificação por chat ID:
- `conversations`: vincula ao `chat_id` do WhatsApp
- `messages`: mensagens organizadas por conversa

## ⚙️ Configurações Úteis

### Ajustar limite de histórico
```python
def modelo_com_historico(history, user_input):
    # Limite as últimas 5 mensagens
    recent = history[-5:]
    # ... processa com seu modelo
    return "resposta"
```

### Mensagens de boas-vindas automáticas
```python
def modelo_com_boas_vindas(history, user_input):
    if not history:  # Primeira mensagem
        return "Olá! Como posso ajudar hoje?"
    return modelo_com_historico(history, user_input)
```

## 🔧 Solução de Problemas

### QR Code não aparece?
- Verifique se `qrcode` está instalado: `pip install qrcode[pil]`
- A imagem é salva em `qrcode_whatsapp.png`

### Conexão falha?
- Certifique-se de que o WhatsApp Web está aberto no celular
- Tente reconectar após 30 segundos

### Memória alta?
- Limite o histórico de mensagens no callback
- Feche conexões não usadas

## 🎨 Personalização

### Adicione saudações personalizadas
```python
def modelo_saudacoes(history, user_input):
    if not history:
        return "Bem-vindo ao nosso chatbot! ✨"
    return model_comum(history, user_input)
```

### Reconheça comandos especiais
```python
COMANDOS = {
    "ajuda": "Estou aqui para ajudar!",
    "sair": "Até mais! 👋"
}

def modelo_comandos(history, user_input):
    if user_input in COMANDOS:
        return COMANDOS[user_input]
    return model_callback(history, user_input)
```

## 📊 Performance Tips

1. **Use `limit` no histórico**: `get_conversation_history(conv_id, limit=5)`
2. **Reutilize instâncias**: Crie um bot global, não por mensagem
3. **Desative callbacks desnecessários**: Mantenha o mínimo de processamento
4. **SQLite pragmático**: O banco já está otimizado para baixo consumo

## 🔗 Links Úteis
- [whatsapp-web.py docs](https://github.com/Jub-Jr/python-whatsapp-web)
- [SQLite PRAGMA settings](https://www.sqlite.org/pragma.html)