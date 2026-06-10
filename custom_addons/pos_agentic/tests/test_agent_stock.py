from odoo.tests.common import TransactionCase

class TestAgentStock(TransactionCase):
    def setUp(self):
        super(TestAgentStock, self).setUp()
        # ARRANGE: Creamos el escenario de prueba (Beliefs)
        self.product = self.env['product.template'].create({
            'name': 'Producto Test Agente',
            'is_agentic_monitored': True,
            'agent_stock_priority': '3',
            'type': 'consu'
        })

    def test_agent_notification(self):
        """Verifica que el agente razona y genera un mensaje"""
        # ACT: Forzamos el razonamiento
        self.env['product.template'].run_agentic_stock_check()
        
        # ASSERT: Verificamos la acción en el Chatter
        messages = self.env['mail.message'].search([
            ('res_id', '=', self.product.id),
            ('model', '=', 'product.template')
        ])
        self.assertTrue(len(messages) > 0, "Error: El agente debería haber publicado una alerta")
