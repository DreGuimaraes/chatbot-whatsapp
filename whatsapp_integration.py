#!/usr/bin/env python3
"""
Integração WhatsApp - Usa whatsapp-web.py para responder mensagens
Requer: pip install whatsapp-web-py
"""

import qrcode
import time
import threading
from typing import Optional, Dict, Any
from whatsapp_integration import LightweightChatbot


class WhatsAppChatbot:
    """Wrapper para usar o chatbot no WhatsApp via whatsapp-web.py."""

    def __init__(self, chatbot: LightweightChatbot, session_file: str = "whatsapp_session.pickle"):
        self.bot = chatbot
        self.session_file = session_file
        self.wa = None
        self.is_connected = False

    def start(self, model_callback=None):
        """Inicializa o WhatsApp Web e conecta."""
        try:
            from whatsapp_web_py.client import Client
            from whatsapp_web_py.session import Session
            from whatsapp_web_py.qr_code import QrCode
        except ImportError:
            print("Instale: pip install whatsapp-web-py")
            return

        # Tenta carregar sessão salva
        session = None
        try:
            session = Session(self.session_file)
            session.load()
        except FileNotFoundError:
            pass

        self.wa = Client(session=session)

        # Define callbacks
        self.wa.on_qr_code = self._on_qr
        self.wa.on_auth_failure = self._on_auth_failure
        self.wa.on_ready = self._on_ready
        self.wa.on_message = lambda message: self._on_message(message, model_callback)

        # Conecta
        self.wa.start()

        # Aguarda conexão
        timeout = 30
        start = time.time()
        while not self.is_connected and (time.time() - start) < timeout:
            time.sleep(0.5)

        if not self.is_connected:
            print("⚠️  Não foi possível conectar no WhatsApp (timeout)")

    def _on_qr(self, qr_code):
        """Exibe QR code para escanear."""
        img = qrcode.make(qr_code)
        img.save("qrcode_whatsapp.png")
        print("📱 Abra o WhatsApp → Configurações → WhatsApp Web → Escaneie o QR abaixo:")
        img.show()  # ou: img.save("qrcode.png") e instruir usuário

    def _on_auth_failure(self, exc):
        print(f"❌ Erro de autenticação: {exc}")

    def _on_ready(self):
        self.is_connected = True
        print("✅ Conectado ao WhatsApp!")

    def _on_message(self, message, model_callback: Optional[callable]):
        """Processa mensagens recebidas."""
        if message.from_me:
            return  # Ignora mensagens enviadas por mim

        print(f"\n📨 Nova mensagem de {message.author.contact.name}: {message.body}")

        # Inicia ou recupera conversa
        chat_id = str(message.chat.id)
        if not hasattr(self, '_conv_cache'):
            self._conv_cache = {}

        if chat_id not in self._conv_cache:
            self._conv_cache[chat_id] = self.bot.start_conversation(session_id=chat_id)

        conv_id = self._conv_cache[chat_id]

        # Gera resposta
        if model_callback:
            resposta = model_callback(
                self.bot.get_conversation_history(conv_id, limit=10),
                message.body
            )
        else:
            resposta = self.bot.generate_response(conv_id, message.body)

        # Envia resposta
        message.reply(resposta)
        print(f"💬 Enviado: {resposta[:50]}...")

    def save_session(self):
        """Salva a sessão do WhatsApp para reconexão rápida."""
        if self.wa and self.is_connected:
            self.wa.session.save(self.session_file)
            print(f"💾 Sessão salva em {self.session_file}")

    def stop(self):
        """Encerra a conexão."""
        if self.wa:
            self.wa.logout()
        self.is_connected = False


if __name__ == "__main__":
    # Exemplo de uso
    bot = LightweightChatbot("whatsapp_chatbot.db")
    wa_bot = WhatsAppChatbot(bot)

    print("Iniciando WhatsApp Chatbot...")
    print("Escaneie o QR code com o WhatsApp no celular")

    # Modo offline: sem modelo personalizado
    wa_bot.start()

    try:
        while wa_bot.is_connected:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Encerrando...")
        wa_bot.save_session()
        wa_bot.stop()