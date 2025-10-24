# verify_api_key.py
import os
import re

def get_openai_api_key() -> str:
    """
    Recupera la API key de OpenAI desde la variable de entorno y valida su formato.
    Lanza excepción si no existe o no parece válida.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("No se encontró la variable de entorno OPENAI_API_KEY.")
    
    # Validación simple: debe empezar con "sk-" y tener al menos 40 caracteres
    if not re.match(r"^sk-[A-Za-z0-9]{40,}$", api_key):
        raise ValueError(
            f"La clave de OpenAI parece inválida: {api_key[:8]}... (revisa tu variable de entorno)"
        )
    
    return api_key

if __name__ == "__main__":
    try:
        key = get_openai_api_key()
        print("✅ La API key parece válida:", key[:8] + "...")
    except ValueError as e:
        print("❌ Error:", e)
