from transformers import pipeline
import traceback

# --- CONFIGURACIÓN E INICIALIZACIÓN DEL MODELO MEJORADO ---
MODEL_NAME = "google/flan-t5-small" # ¡CAMBIADO A 'base' para mayor capacidad!

try:
    print(f"Cargando modelo de IA ({MODEL_NAME})...")
    # Asegúrate de tener suficiente memoria RAM/VRAM para este modelo
    generator = pipeline("text2text-generation", model=MODEL_NAME)
    print("Modelo de IA cargado con éxito.")
except Exception as e:
    print(f"ERROR: Fallo al cargar el modelo de IA. El asistente no funcionará. Detalles: {str(e)}")
    generator = None 

# Definimos una respuesta de fallback segura en español
FALLBACK_RESPONSE = "Recomendación: Se recomienda un tratamiento personalizado (hidratación o nutrición) mientras se analiza mejor su consulta."

def analizar_visita_con_ia(cliente, servicio):
    if generator is None:
        return "Recomendación: ERROR - El sistema de IA no está disponible."
        
    # --- PROMPT SIMPLIFICADO Y DIRECTO ---
    # Los modelos T5 funcionan mejor con instrucciones claras y concisas.
    prompt = (
        "Actúa como una experta en belleza y asesora a un cliente de un salón. "
        "Basado en la siguiente consulta, recomienda de forma profesional y detallada un único servicio de belleza adecuado. "
        "Responde SOLAMENTE la recomendación, en español. No repitas la pregunta.\n\n"
        
        f"Consulta del cliente: {servicio}"
    )

    try:
        # Debugging
        print("-" * 50)
        print("PROMPT FINAL ENVIADO A LA IA:", prompt) 
        
        # Generación de la respuesta con parámetros ajustados para calidad
        respuesta_ia = generator(
            prompt, 
            max_length=150,           # Reducido para enfoque
            temperature=0.7,          # Mantener la variedad
            do_sample=True,           
            num_return_sequences=1
        )[0]['generated_text'] 
        
        print("Respuesta cruda de la IA:", respuesta_ia)
        print("-" * 50)

        # LÓGICA DE LIMPIEZA Y FORMATEO
        respuesta_formateada = respuesta_ia.strip()
        
        # Eliminamos cualquier prefijo no deseado que el modelo pueda haber generado
        limpiar_prefijos = ["recomendación:", "recomendacion:", "respuesta:", "asesora:", "aquí está la recomendación:"]
        for prefijo in limpiar_prefijos:
            if respuesta_formateada.lower().startswith(prefijo):
                respuesta_formateada = respuesta_formateada[len(prefijo):].strip()
        
        # 1. Verificación básica
        if not respuesta_formateada or len(respuesta_formateada) < 10:
            return FALLBACK_RESPONSE
            
        # 2. Seguridad contra la contaminación lingüística (Inglés, etc.)
        if any(cont in respuesta_formateada.lower() for cont in ["i recommend", "the recommendation"]):
            print("DEBUG: Respuesta contaminada detectada. Usando fallback.")
            return FALLBACK_RESPONSE
            
        # 3. Retorno final, asegurando el prefijo
        return "Recomendación: " + respuesta_formateada

    # MANEJO DE EXCEPCIONES
    except Exception as e:
        print("ERROR IA REAL:", str(e))
        print("Traceback completo:", traceback.format_exc())
        return f"Recomendación: Error interno. {FALLBACK_RESPONSE}"