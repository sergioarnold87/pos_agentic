import os
import httpx
import xmlrpc.client
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, UploadFile, File
from dotenv import load_dotenv

# Nuevas importaciones para Google Vertex AI (Gemini)
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# 1. Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(title="Agentic POS Middleware")

# ==============================================================================
# CONFIGURACIÓN DE GOOGLE VERTEX AI (El Cerebro)
# ==============================================================================
GCP_PROJECT = os.getenv("GCP_PROJECT", "arandubot")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")

# Inicializamos la conexión con Google Cloud usando tus credenciales locales
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
# Usamos Gemini 1.5 Flash: optimizado para lectura rápida de imágenes y documentos
vision_model = GenerativeModel("gemini-1.5-flash")

# ==============================================================================
# CONFIGURACIÓN DE NTFY (Notificaciones Push)
# ==============================================================================
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "default_fallback_topic")
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

async def send_push_notification(title: str, message: str, priority: str = "default"):
    """Envía notificaciones push al celular del dueño."""
    headers = {"Title": title, "Priority": priority, "Tags": "robot,rotating_light"}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(NTFY_URL, data=message.encode('utf-8'), headers=headers)
            print(f"[AGENT LOG] Success! External voice routed to topic: {NTFY_TOPIC}")
        except Exception as e:
            print(f"[AGENT ERROR] Network failure reaching ntfy.sh: {e}")

# ==============================================================================
# CONFIGURACIÓN DE ODOO (El puente XML-RPC)
# ==============================================================================
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# ==============================================================================
# ENDPOINTS (Las puertas de entrada al Middleware)
# ==============================================================================

@app.post("/api/v1/agent/leer-factura")
async def leer_factura_proveedor(file: UploadFile = File(...)):
    """
    Los 'Ojos' del Agente: Recibe una foto, la procesa con Gemini
    y extrae los productos en formato JSON.
    """
    try:
        # 1. Leemos la imagen subida
        image_content = await file.read()
        image_part = Part.from_data(data=image_content, mime_type=file.content_type)
        
        # 2. El Prompt (Instrucciones precisas para Arandubot)
        prompt = """
        Eres un experto analista de inventario en Paraguay. 
        Analiza esta imagen de una factura o ticket de compra.
        Extrae los productos y devuelve ÚNICAMENTE un JSON válido con la siguiente estructura exacta:
        {
            "proveedor": "Nombre del Proveedor",
            "productos": [
                {"nombre": "Nombre del producto", "cantidad": 0, "precio_unitario": 0.0}
            ]
        }
        No agregues texto introductorio, ni saludos, ni marcas de código Markdown (como ```json).
        """
        
        # 3. Consulta a la IA de Google
        response = vision_model.generate_content([image_part, prompt])
        
        return {
            "status": "success",
            "filename": file.filename,
            "ia_analysis": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento de IA: {str(e)}")


@app.post("/api/v1/agent/webhook")
async def handle_odoo_signal(request: Request, background_tasks: BackgroundTasks):
    """Recibe la alerta de stock crítico desde Odoo y manda un Push al celular."""
    payload = await request.json()
    
    product_name = payload.get("product_name", "Unknown Product")
    stock_level = payload.get("stock_level", 0)
    agent_intent = payload.get("intent", "Manual review required")
    priority_level = payload.get("agent_stock_priority", "default")
    
    ntfy_priority = "high" if priority_level == "critical" else "default"
    title = f"Agentic Alert: {product_name}"
    message = f"Stock level at {stock_level} units. Agent Intention: {agent_intent}"
    
    background_tasks.add_task(send_push_notification, title, message, ntfy_priority)
    return {"status": "success", "message": "Signal received. Processing in background."}


@app.get("/test-odoo")
def test_odoo_connection():
    """Prueba que el Middleware pueda iniciar sesión en Odoo."""
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
        if uid:
            return {"connection": "success", "message": f"¡Puente establecido! UID: {uid}"}
        raise HTTPException(status_code=401, detail="Fallo de autenticación.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando a Odoo: {str(e)}")


@app.get("/test-create-product")
def test_create_product():
    """Prueba que el Middleware pueda escribir/crear un producto en aranduPOS."""
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
        
        if not uid:
            raise HTTPException(status_code=401, detail="Fallo de autenticación.")

        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        nuevo_producto = {
            'name': '🤖 Arandubot Test Product',
            'type': 'consu',
            'list_price': 15000.0,
            'default_code': 'BOT-001'
        }

        product_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.product', 'create',
            [nuevo_producto]
        )

        return {
            "status": "success",
            "message": "¡Agente ejecutó acción con éxito!",
            "odoo_product_id": product_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en Odoo: {str(e)}")