# -*- coding: utf-8 -*-
{
    'name': "Document Quantity Total",

    'summary': """
        Quantity Total for Documents include:
        - Purchase Order
        - Sale Order
        - Picking (Receipt/Transfer/Delivery Order)
        """,

    'description': """
        Quantity and Weight Total on Documents
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    "live_test_url": "https://www.youtube.com/watch?v=qjk0Lbg_5pM",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_invoice_views.xml',
        'report/purchase_order_document_template.xml',
        'report/sale_order_document_template.xml',
        'report/delivery_slip_document_template.xml',
        'report/invoice_document_template.xml',
    ],
    "images":  ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
