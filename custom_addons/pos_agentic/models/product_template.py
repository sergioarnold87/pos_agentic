from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template' # Heredamos del modelo base de Odoo

    # Campos específicos para la Ontología de tu Agente
    is_agentic_monitored = fields.Boolean(
        string="Monitoreado por IA", 
        default=True,
        help="Si está marcado, el Agente de Kiosko vigilará este producto proactivamente."
    )
    agent_stock_priority = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Crítica')
    ], string="Prioridad para el Agente", default='medium')