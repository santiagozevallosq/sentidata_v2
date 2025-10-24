from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def classify_relevance_for_mivivienda(text: str, model: str = "gpt-4o-mini") -> str:
    """
    Analiza un solo texto utilizando un modelo LLM de OpenAI.
    Determina si el contenido es relevante para el Ministerio de Vivienda.
    """
    if not text:
        return "No se proporcionó texto"

    prompt = f"""
Eres un analista del Ministerio de Vivienda, Construcción y Saneamiento del Perú.
Tu tarea es determinar si un texto o publicación es RELEVANTE o NO RELEVANTE
para los intereses del ministerio.

Responde solo con una de las siguientes opciones:
- "RELEVANTE"
- "NO RELEVANTE"

Texto a analizar:
{text}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un experto analista en clasificación de contenido para entidades del Estado peruano."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        message = response.choices[0].message if response.choices else None
        content = getattr(message, "content", None)

        return content.strip() if isinstance(content, str) else "No se obtuvo respuesta del modelo."

    except Exception as e:
        return f"Error al analizar el texto: {str(e)}"
