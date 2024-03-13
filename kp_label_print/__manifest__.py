# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

{
    'name': 'Label Print',
    "version": "14.0.1.0",
    'author': 'Anuraj',
    'category': 'product',
    'summary': 'Label print in lot/serial number',
    'description': 'Label print in lot/serial number',
    'depends': ['stock','base','product'],
    'data': [
        'report/report.xml',
        'report/stock_lot_label.xml',
        'views/company_view.xml',
        'views/product_view.xml',
        'views/stock_production_lot_view.xml',

             ],
}
