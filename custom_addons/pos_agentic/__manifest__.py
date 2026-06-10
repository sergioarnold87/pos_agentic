{
    'name': 'Agentic Kiosk POS',
    'version': '18.0.1.0.0',
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
        'data/ir_cron_data.xml',  # <--- Agrega esta línea
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
