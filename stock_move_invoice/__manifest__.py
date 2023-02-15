

{
    'name': "Invoice From Stock Picking",
    'version': '14.0.1.0.1',
    'summary': """In this module creating customer invoice,vendor bill, customer
    credit note and refund from stock picking""",
    'description': """In this module creating customer invoice,vendor bill, customer
    credit note and refund from stock picking""",
    'category': 'Stock',
    'author': 'Ahmed Hussein',
    'company': '',
    'website': "",
    'depends': ['stock', 'account'],
    'data': [
        'views/account_move_inherited.xml',
        'views/stock_picking_inherited.xml',
        'views/res_config_settings_inherited.xml',
        'wizard/picking_invoice_wizard.xml',
    ],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
