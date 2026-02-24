from openai import OpenAI
import os
import base64


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def detect_car_from_image_bytes(image_bytes: bytes) -> dict:
    """
    Devuelve: {"make": str, "model": str, "confidence": float}
    """
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Eres un sistema de visión que identifica coches en una imagen. "
                    "Devuelve SOLO JSON válido con claves: make, model, confidence (0-1)."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Identifica la marca y modelo del coche."},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{b64}",
                    },
                ],
            },
        ],
    )

    # resp.output_text suele devolver el texto final del modelo
    text = resp.output_text.strip()

    # Intentamos parsear JSON de forma simple
    import json
    return json.loads(text)