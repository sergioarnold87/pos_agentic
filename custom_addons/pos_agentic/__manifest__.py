{
    'name': 'Agentic Kiosk POS',
    'version': '16.0.1.0.1',  # <--- BUMP DE VERSIÓN (Termina en 1)
    'category': 'Sales/Point of Sale',
    'summary': 'Proactive POS with Retail AI Agents',
    'description': """
        Integrates Odoo POS with Agentic AI principles for proactive 
        retail management, including automated stock reasoning.
    """,
    'author': 'Sergio',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'stock'],
    'data': [
        'views/product_template_views.xml',
        'data/ir_cron_data.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            # EL TRUCO DEL COMODÍN: Carga todo lo que haya en src y sus subcarpetas [cite: 6401, 6411]
            'pos_agentic/static/src/**/*', 
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}