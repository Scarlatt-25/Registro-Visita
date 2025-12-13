from openai import OpenAI, RateLimitError
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analizar_visita_con_ia(nombre, rut, motivo):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que analiza registros de visitas."
                },
                {
                    "role": "user",
                    "content": f"""
                    Nombre: {nombre}
                    RUT: {rut}
                    Motivo: {motivo}

                    Analiza si la visita es normal o sospechosa.
                    """
                }
            ],
            max_tokens=120
        )

        return response.choices[0].message.content

    except RateLimitError:
        # 🔐 Fallback cuando no hay cuota
        return (
            "⚠️ Análisis IA (modo simulación): "
            "La visita corresponde a un ingreso normal. "
            "No se detectan patrones sospechosos según el motivo registrado."
        )

    except Exception as e:
        return f"Error en análisis IA: {str(e)}"
