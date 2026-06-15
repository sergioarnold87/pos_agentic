from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_agentic_monitored = fields.Boolean(string="Monitoreado por IA", default=False)
    agent_stock_priority = fields.Selection([
        ('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'), ('3', 'Crítica')
    ], string="Prioridad para el Agente", default='0')

    @api.model
    def run_agentic_stock_check(self):
        _logger.info("Agente IA: Iniciando ciclo de razonamiento...")
        products = self.search([('is_agentic_monitored', '=', True)])
        for product in products:
            if product.agent_stock_priority == '3' and product.qty_available < 10:
                # 1. Chatter (Voz Interna)
                product.message_post(body=f"🚀 ALERTA: Stock crítico ({product.qty_available})")
                
                # 2. Webhook (Voz Externa - Contrato API Corregido)
                try:
                    # Ruta corregida para coincidir con FastAPI
                    middleware_url = "http://172.17.0.1:8000/api/v1/agent/webhook"
                    
                    # Diccionario JSON corregido para coincidir con las llaves que espera FastAPI
                    payload = {
                        "product_name": product.name,
                        "stock_level": product.qty_available,
                        "intent": "Generar orden de abastecimiento automático",
                        "agent_stock_priority": "critical"
                    }
                    
                    requests.post(middleware_url, json=payload, timeout=2)
                    _logger.info(f"✅ Señal enviada al middleware para: {product.name}")
                except Exception as e:
                    _logger.error(f"❌ Error de conexión: {e}")
