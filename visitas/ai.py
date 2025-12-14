from transformers import pipeline
import traceback

# --- CONFIGURACIÓN E INICIALIZACIÓN DEL MODELO (CRÍTICO) ---
# Cambia a un modelo más grande o en español para mejores resultados.
# Opciones: 'google/flan-t5-base' (mejor que small), o 'mrm8488/t5-base-finetuned-spanish' para español nativo.
try:
    print("Cargando modelo de IA (google/flan-t5-small)...")  # Cambié a base para más capacidad
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    print("Modelo de IA cargado con éxito.")
except Exception as e:
    print(f"ERROR: Fallo al cargar el modelo de IA. El asistente no funcionará. Detalles: {str(e)}")
    generator = None 

# Definimos una respuesta de fallback segura en español
FALLBACK_RESPONSE = "Recomendación: Se recomienda un tratamiento personalizado (hidratación o nutrición) mientras se analiza mejor su consulta."

def analizar_visita_con_ia(cliente, servicio):
    # Verificación de carga inicial
    if generator is None:
        return "Recomendación: ERROR - El sistema de IA no está disponible. Por favor, reinicie el servidor."
        
    # --- PROMPT MEJORADO: AGREGAMOS EJEMPLOS (FEW-SHOT) Y CLARIDAD ---
    # Incluimos ejemplos para guiar al modelo y forzamos español puro.
    prompt = (
        "Eres una experta en un salón de belleza. Responde solo en español, de manera profesional y detallada. "
        "Recomienda un servicio basado en la consulta del cliente. No repitas las instrucciones ni el prompt.\n\n"
        
        "Ejemplo 1:\n"
        "Consulta del cliente: Tengo el cabello dañado por el sol, ¿qué recomiendas?\n"
        "Recomendación: Para reparar el cabello dañado por el sol, recomendamos el Tratamiento de Reparación con Keratina. Este servicio fortalece la fibra capilar, restaura la elasticidad y previene futuras roturas.\n\n"
        
        "Ejemplo 2:\n"
        "Consulta del cliente: Quiero un corte moderno para mi cabello largo.\n"
        "Recomendación: Para un corte moderno en cabello largo, recomendamos el Corte Asimétrico con Capas. Este estilo añade movimiento, resalta los rasgos faciales y es fácil de mantener.\n\n"
        
        f"Consulta del cliente: {servicio}\n\n"
        "Recomendación:"
    )

    try:
        # Debugging: Muestra el prompt antes de llamar al modelo
        print("-" * 50)
        print("PROMPT FINAL ENVIADO A LA IA:", prompt) 
        
        # Generación de la respuesta con parámetros ajustados para más creatividad
        respuesta_ia = generator(
            prompt, 
            max_length=200, 
            temperature=0.7,  # Añadido: Hace respuestas más variadas
            do_sample=True,   # Añadido: Activa muestreo para evitar repeticiones
            num_return_sequences=1
        )[0]['generated_text'] 
        print("Respuesta cruda de la IA:", respuesta_ia)
        print("-" * 50)

        # LÓGICA DE RETORNO Y FORMATEO MEJORADA
        
        # 1. Si la respuesta está vacía o es demasiado corta, usa el fallback.
        if not respuesta_ia or len(respuesta_ia.strip()) < 10:
            return FALLBACK_RESPONSE

        respuesta_formateada = respuesta_ia.strip()
        
        # 2. Seguridad contra la contaminación lingüística (ampliada)
        contaminaciones = ["i have", "the respuesta", "eres an expert", "consulta del cliente", "recommend a professional"]
        if any(cont in respuesta_formateada.lower() for cont in contaminaciones):
            print("DEBUG: Respuesta contaminada detectada. Usando fallback.")
            return FALLBACK_RESPONSE
            
        # 3. Forzamos el prefijo 'Recomendación: ' si el modelo no lo generó.
        if not respuesta_formateada.lower().startswith("recomendación:"):
            return "Recomendación: " + respuesta_formateada
             
        # Si todo está bien
        return respuesta_formateada

    # MANEJO DE EXCEPCIONES
    except Exception as e:
        print("ERROR IA REAL:", str(e))
        print("Traceback completo:", traceback.format_exc())
        return f"Recomendación: Error interno. {FALLBACK_RESPONSE}"