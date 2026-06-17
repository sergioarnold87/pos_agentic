from fastapi import FastAPI, UploadFile, File, HTTPException
from google import genai
from google.genai import types
import json

# Inicializamos la app de FastAPI
app = FastAPI(title="Analizador de Facturas con Gemini")

# 1. Inicializar el cliente con el SDK moderno apuntando a tu proyecto
client = genai.Client(
    vertexai=True, 
    project="arandubot", 
    location="us-central1"
)

@app.post("/procesar-factura/")
async def procesar_factura(file: UploadFile = File(...)):
    # Validamos que el archivo sea una imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo subido debe ser una imagen.")

    try:
        # Leer los bytes de la imagen recibida en FastAPI
        image_bytes = await file.read()
        
        # 2. Preparar la imagen para el formato que exige el nuevo SDK
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=file.content_type
        )
        
        # 3. Definir las instrucciones claras (Prompt)
        prompt = """
        Eres un asistente experto en contabilidad y auditoría visual de documentos, especializado en facturas de Paraguay. 
        Analiza con muchísimo detenimiento la imagen de esta factura.
        Extrae la siguiente información y devuélvela estrictamente en formato JSON con estas claves exactas:
        - "emisor": Nombre de la empresa o persona que emite la factura (ej: Agroveterinaria EL TOKE).
        - "ruc_emisor": El número de RUC del emisor (incluyendo el dígito verificador).
        - "timbrado": El número de timbrado de la factura.
        - "numero_factura": El número completo de la factura (ej: 001-001-0089038).
        - "condicion_venta": Si es "CONTADO" o "CREDITO".
        - "fecha": Fecha de emisión. Presta especial atención y lee con ultra-precisión los dígitos del día y del mes (asegúrate de no confundir un 5 con un 6). Devuélvela en formato YYYY-MM-DD.
        - "total": Monto total a pagar (solo el número, sin puntos ni comas, ej: 48000).
        - "total_iva_10": El monto total de la liquidación del IVA 10% (solo el número, ej: 4364). Si no hay, pon 0.
        - "items": Una lista de los productos/servicios donde cada uno tenga "descripcion", "cantidad", y "precio_unitario" (solo números).
        """

        # 4. Forzar a que el modelo responda EXCLUSIVAMENTE con un JSON válido
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1 # Temperatura baja para que sea preciso y no invente datos
        )

        # 5. Llamar al modelo Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, prompt],
            config=config
        )

        # 6. Parsear el texto devuelto a un diccionario de Python y enviarlo al cliente
        datos_extraidos = json.loads(response.text)
        return {"status": "success", "data": datos_extraidos}

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="La IA no devolvió un JSON válido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento de IA: {str(e)}")
        