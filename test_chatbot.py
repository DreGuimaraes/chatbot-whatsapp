#!/usr/bin/env python3
"""Testes básicos do chatbot."""

import unittest
import os
from chatbot import LightweightChatbot


class TestLightweightChatbot(unittest.TestCase):
    """Testes unitários do chatbot."""

    def setUp(self):
        """Configura testes com banco de dados temporário."""
        self.test_db = "test_chatbot_temp.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.bot = LightweightChatbot(self.test_db)

    def tearDown(self):
        """Limpa banco de dados de teste."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_inicia_conversa(self):
        """Testa criação de conversa."""
        conv_id = self.bot.start_conversation()
        self.assertIsInstance(conv_id, int)
        self.assertGreater(conv_id, 0)

    def test_adiciona_mensagem(self):
        """Testa adição de mensagens."""
        conv_id = self.bot.start_conversation()
        msg_id = self.bot.add_message(conv_id, "user", "Teste")
        self.assertIsInstance(msg_id, int)
        self.assertGreater(msg_id, 0)

    def test_recupera_historico(self):
        """Testa recuperação de histórico."""
        conv_id = self.bot.start_conversation()
        self.bot.add_message(conv_id, "user", "Olá")
        self.bot.add_message(conv_id, "assistant", "Tudo bem")

        history = self.bot.get_conversation_history(conv_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['role'], 'user')
        self.assertEqual(history[1]['role'], 'assistant')

    def test_generate_response_sem_callback(self):
        """Testa geração de resposta sem modelo externo."""
        conv_id = self.bot.start_conversation()
        resposta = self.bot.generate_response(conv_id, "Olá")
        self.assertIsInstance(resposta, str)
        self.assertTrue(len(resposta) > 0)

    def test_stats(self):
        """Testa estatísticas."""
        conv_id = self.bot.start_conversation()
        self.bot.add_message(conv_id, "user", "Teste")

        stats = self.bot.get_stats()
        self.assertEqual(stats['conversations'], 1)
        self.assertEqual(stats['messages'], 1)


if __name__ == "__main__":
    unittest.main()