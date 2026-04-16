#!/usr/bin/env python3
"""
Script de setup completo - inicializa tudo para usar o chatbot no WhatsApp
"""

import os
import subprocess
import sys

def check_install(package):
    """Verifica se um pacote está instalado."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_package(package):
    """Instala um pacote via pip."""
    print(f"📦 Instalando {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setup():
    print("🔧 Setup do Chatbot WhatsApp")
    print("=" * 40)

    # Verifica e instala dependências
    dependencies = {
        "whatsapp_web_py": "whatsapp-web-py",
        "qrcode": "qrcode[pil]",
    }

    for pkg_name, pkg_install in dependencies.items():
        if not check_install(pkg_name):
            install_package(pkg_install)
        else:
            print(f"✅ {pkg_name} já instalado")

    # Verifica o pacote principal
    if not check_install("chatbot"):
        print("📦 Instalando o pacote do chatbot...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    else:
        print("✅ chatbot já instalado")

    print("\n" + "=" * 40)
    print("✅ Setup completo!")
    print("\n📖 Leia INTEGRATION_GUIDE.md para começar")
    print("💻 Execute: python smart_whatsapp_chatbot.py")

if __name__ == "__main__":
    setup()