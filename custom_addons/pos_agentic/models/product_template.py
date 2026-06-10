from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_agentic_monitored = fields.Boolean(string="Monitoreado por IA", default=False)
    agent_stock_priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
        ('3', 'Crítica')
    ], string="Prioridad para el Agente", default='0')

    @api.model
    def run_agentic_stock_check(self):
        """
        Método de Razonamiento Agéntico:
        Percibe el stock y decide si debe alertar.
        """
        _logger.info("Agente de IA: Iniciando ciclo de razonamiento de stock...")
        
        # 1. PERCIBIR: Buscamos productos marcados para monitoreo
        products_to_monitor = self.search([('is_agentic_monitored', '=', True)])
        
        for product in products_to_monitor:
            # 2. RAZONAR: Lógica basada en prioridades
            # Umbral simple: si es prioridad Crítica (3) y hay menos de 10 unidades
            if product.agent_stock_priority == '3' and product.qty_available < 10:
                # 3. ACTUAR: Publicar en el Chatter (muro del producto)
                product.message_post(
                    body=f"🚀 **ALERTA AGÉNTICA**: El producto '{product.name}' tiene stock crítico ({product.qty_available}). ¡Es necesario reabastecer!",
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment'
                )
                _logger.warning(f"Agente de IA: Intención de reabastecimiento generada para {product.name}")
