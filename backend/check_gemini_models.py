"""
Script para verificar los modelos disponibles de Gemini
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

# Configurar API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY no encontrada")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Modelos disponibles con tu API key:\n")
print("-" * 70)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Descripción: {model.display_name}")
        print(f"   Métodos: {', '.join(model.supported_generation_methods)}")
        print()

print("-" * 70)
print("\n💡 Usa el nombre completo (ej: 'models/gemini-pro') o solo el sufijo (ej: 'gemini-pro')")
