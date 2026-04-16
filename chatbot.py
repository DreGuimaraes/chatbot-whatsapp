#!/usr/bin/env python3
"""
Chatbot leve com SQLite - Otimizado para ambientes com recursos limitados
Requer apenas Python padrão + SQLite3
"""

import sqlite3
import json
import datetime
from typing import Optional, List, Dict, Any
import hashlib


class LightweightChatbot:
    """Chatbot minimalista com armazenamento SQLite otimizado para baixo consumo de recursos."""

    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Inicializa o banco de dados SQLite com tabelas mínimas."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        # Índices para melhor performance
        conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)")
        conn.commit()
        conn.close()

    def _get_conn(self):
        """Retorna uma conexão leve com SQLite."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")  # Melhora performance em ambientes concorrentes
        conn.row_factory = sqlite3.Row
        return conn

    def start_conversation(self, session_id: Optional[str] = None, metadata: Optional[Dict] = None) -> int:
        """Inicia uma nova conversa."""
        if session_id is None:
            session_id = hashlib.md5(datetime.datetime.now().isoformat().encode()).hexdigest()[:16]

        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (session_id, created_at, metadata) VALUES (?, ?, ?)",
            (session_id, datetime.datetime.now().isoformat(), json.dumps(metadata or {}))
        )
        conv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return conv_id

    def add_message(self, conversation_id: int, role: str, content: str) -> int:
        """Adiciona uma mensagem à conversa."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (conversation_id, role, content, datetime.datetime.now().isoformat())
        )
        msg_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return msg_id

    def get_conversation_history(self, conversation_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Recupera o histórico de uma conversa."""
        conn = self._get_conn()
        cursor = conn.cursor()

        query = "SELECT role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY id"
        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, (conversation_id,))
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def generate_response(self, conversation_id: int, user_input: str,
                         model_callback=None) -> str:
        """
        Gera uma resposta para a entrada do usuário.
        model_callback: função opcional para processamento real (ex: LLM API)
        """
        # Adiciona mensagem do usuário
        self.add_message(conversation_id, "user", user_input)

        # Obtém histórico da conversa
        history = self.get_conversation_history(conversation_id, limit=10)

        # Se callback fornecido, usa modelo externo
        if model_callback:
            response = model_callback(history, user_input)
        else:
            # Resposta padrão (placeholder - substituir por modelo real)
            response = self._default_response(history, user_input)

        # Adiciona resposta do assistente
        self.add_message(conversation_id, "assistant", response)
        return response

    def _default_response(self, history: List[Dict], user_input: str) -> str:
        """Resposta padrão minimalista."""
        # Lógica simples de eco - substituir por modelo real
        if "olá" in user_input.lower() or "oi" in user_input.lower():
            return "Olá! Como posso ajudar?"
        elif "obrigado" in user_input.lower() or "valeu" in user_input.lower():
            return "De nada!"
        return "Entendi. Precisa de mais alguma coisa?"

    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do banco de dados."""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM conversations")
        conv_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM messages")
        msg_count = cursor.fetchone()['count']

        conn.close()
        return {"conversations": conv_count, "messages": msg_count}


if __name__ == "__main__":
    # Exemplo de uso
    bot = LightweightChatbot()

    # Inicia conversa
    conv_id = bot.start_conversation()
    print(f"Conversa iniciada: {conv_id}")

    # Simula interação
    resposta = bot.generate_response(conv_id, "Olá, como vai?")
    print(f"Bot: {resposta}")

    resposta = bot.generate_response(conv_id, "Tudo bem, obrigado!")
    print(f"Bot: {resposta}")

    # Estatísticas
    stats = bot.get_stats()
    print(f"Estatísticas: {stats}")