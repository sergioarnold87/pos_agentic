from odoo.tests import common

class TestAgentStock(common.TransactionCase):
    def setUp(self):
        super(TestAgentStock, self).setUp()
        # Creamos un producto de prueba (Belief)
        self.product = self.env['product.template'].create({
            'name': 'Producto Test Agente',
            'is_agentic_monitored': True,
            'agent_stock_priority': '3', # Crítica
            'type': 'consu' # Producto consumible para el test
        })

    def test_agent_notification(self):
        """Verifica que el agente razona y genera un mensaje"""
        # Ejecutamos el método del cerebro
        self.env['product.template'].run_agentic_stock_check()
        
        # Percibimos si el mensaje se publicó en el Chatter
        messages = self.env['mail.message'].search([
            ('res_id', '=', self.product.id),
            ('model', '=', 'product.template')
        ])
        self.assertTrue(len(messages) > 0, "El agente debería haber publicado una alerta")
