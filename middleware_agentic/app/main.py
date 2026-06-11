from fastapi import FastAPI, Request
import logging

app = FastAPI(title="Kiosko Agentic Middleware")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def health_check():
    return {"status": "Cerebro Operativo", "agente": "Listo para WhatsApp"}

@app.post("/webhook/odoo_stock_alert")
async def receive_odoo_alert(request: Request):
    """
    Recibe la intención de reabastecimiento desde Odoo.
    """
    data = await request.json()
    product_name = data.get('product_name', 'Producto Desconocido')
    stock_qty = data.get('stock_qty', 0)
    
    logger.info(f"🚀 CEREBRO: Recibida alerta de stock para {product_name} ({stock_qty} unidades)")
    
    # Próximo paso: Aquí dispararemos el mensaje a WhatsApp
    return {"message": "Alerta capturada por el Cerebro de Orquestación"}
