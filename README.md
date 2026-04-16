# Chatbot Leve com SQLite

## Visão geral
Implementação minimalista de chatbot otimizada para ambientes com recursos limitados (ex: 2GB RAM), usando apenas Python padrão + SQLite3.

## Características
- Armazenamento local com SQLite (arquivo único: `chatbot.db`)
- Baixo consumo de memória
- Sem dependências externas
- Índices otimizados para performance
- Suporte a múltiplas conversas simultâneas

## Estrutura do banco de dados
- `conversations`: armazena sessões de conversa
- `messages`: armazena mensagens (user/assistant)

## Uso
```python
from chatbot import LightweightChatbot

bot = LightweightChatbot()
conv_id = bot.start_conversation()

# Modo simples (sem modelo externo)
resposta = bot.generate_response(conv_id, "Olá!")

# Com callback de modelo personalizado
def meu_modelo(history, user_input):
    # Implementar lógica do seu modelo aqui
    return "Resposta personalizada"

resposta = bot.generate_response(conv_id, "Me diga algo", meu_modelo)
```

## Configuração
- Banco de dados: `chatbot.db` (no diretório atual)
- Sem configuração necessária