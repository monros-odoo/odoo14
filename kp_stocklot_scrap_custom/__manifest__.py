# -*- coding: utf-8 -*-

{
    'name': 'Stock - Lot Scrap Custom',
    'version': '14.0.1.1.0',
    'category': 'General',
    'summary': "Module for lot-scrap functionality",
    'author': 'KP/Anju',
    'description': """
        Module for create the scrap transfer from Lot Lots
        """,
    'depends': ['base','stock'],
    'data': [
        'views/stock_production_lot.xml',
        'views/res_company.xml',
        # 'views/stock_assests.xml',
        'views/stock_picking.xml',
    ],
    'qweb': [
        # 'static/src/xml/make_scrap_transfer_button.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
