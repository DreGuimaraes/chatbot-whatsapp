#!/usr/bin/env python3
"""
Exemplo avançado de chatbot WhatsApp com reconhecimento de comandos
"""

import os
import sys
import json
from typing import Optional, List, Dict, Any

# Adiciona src ao path se existir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import LightweightChatbot
from whatsapp_integration import WhatsAppChatbot


class SmartWhatsAppChatbot:
    """Chatbot inteligente com reconhecimento de comandos para WhatsApp."""

    def __init__(self, db_path: str = "smart_whatsapp.db"):
        self.bot = LightweightChatbot(db_path)
        self.wa_bot = WhatsAppChatbot(self.bot)

        # Comandos reconhecidos
        self.commands = {
            "ajuda": self.cmd_help,
            "olá": self.cmd_hello,
            "tudo bem": self.cmd_hello,
            "saudação": self.cmd_hello,
            "h": self.cmd_help,
            "?": self.cmd_help,
            "obrigado": self.cmd_thanks,
            "obrigada": self.cmd_thanks,
            "vlw": self.cmd_thanks,
            "tchau": self.cmd_goodbye,
            "adeus": self.cmd_goodbye,
            "sair": self.cmd_goodbye,
            "status": self.cmd_status,
            "info": self.cmd_info,
        }

    # --- Comandos do bot ---
    def cmd_help(self, history: List[Dict], user_input: str) -> str:
        """Mostra ajuda dos comandos disponíveis."""
        cmd_list = "\n".join([f"  • `{cmd}` → {desc}" for cmd, (_, desc) in self.commands.items() if desc])
        return (
            "🤖 **Comandos disponíveis:**\n"
            f"{cmd_list}\n\n"
            "Envie qualquer mensagem para conversar normalmente!"
        )

    def cmd_hello(self, history: List[Dict], user_input: str) -> str:
        """Saudação padrão."""
        return "👋 Olá! Como posso te ajudar hoje?"

    def cmd_thanks(self, history: List[Dict], user_input: str) -> str:
        """Resposta de agradecimento."""
        return "👨‍💻 De nada! Fico feliz em ajudar."

    def cmd_goodbye(self, history: List[Dict], user_input: str) -> str:
        """Despedida."""
        return "👋 Até mais! Qualquer coisa, estou aqui!"

    def cmd_status(self, history: List[Dict], user_input: str) -> str:
        """Mostra estatísticas do bot."""
        stats = self.bot.get_stats()
        return f"📊 **Status:**\nConversas: {stats['conversations']}\nMensagens: {stats['messages']}"

    def cmd_info(self, history: List[Dict], user_input: str) -> str:
        """Informações sobre o bot."""
        return (
            "ℹ️ **Sobre este bot:**\n"
            "Chatbot leve com SQLite\n"
            "Totalmente offline\n"
            "Sem dependências externas"
        )

    def recognize_command(self, text: str) -> Optional[tuple]:
        """Reconhece comandos e retorna (handler, matched_command)."""
        text_lower = text.lower().strip()

        # Verifica comandos exatos
        for cmd, (handler, _) in self.commands.items():
            if text_lower == cmd:
                return handler, cmd

        # Verifica comandos que iniciam com texto
        for cmd, (handler, _) in self.commands.items():
            if text_lower.startswith(cmd + " "):
                return handler, cmd

        return None, None

    def generate_response(self, conversation_id: int, user_input: str) -> str:
        """Gera resposta com reconhecimento de comandos."""
        # Tenta reconhecer comando
        handler, matched_cmd = self.recognize_command(user_input)

        if handler:
            return handler([], user_input)

        # Usa modelo padrão se não for comando
        return self.bot._default_response([], user_input)

    def start_whatsapp(self):
        """Inicia a integração com WhatsApp."""
        self.wa_bot.start(model_callback=self.generate_response)


if __name__ == "__main__":
    print("🚀 Iniciando Smart Chatbot WhatsApp...")

    chatbot = SmartWhatsAppChatbot()

    print("📱 Inicie o WhatsApp e escaneie o QR code")
    print("💾 Sessão salva automaticamente para reconexão")
    print()

    try:
        chatbot.start_whatsapp()

        # Mantém rodando
        while chatbot.wa_bot.is_connected:
            import time
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n⏹️  Encerrando...")
        chatbot.wa_bot.save_session()
        chatbot.wa_bot.stop()
        print("✅ Finalizado!")