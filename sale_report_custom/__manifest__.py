# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Report Custom',
    'version': '14.0.1.1.0',
    'category': 'Sales Management',
    'summary': "Customization the Sale Report",
    'author': 'KP/Anju',
    'description': """
        Customization of the Sale Report
        """,
    'depends': ['sale', 'de_document_quantity_total'],
    'data': [
        'report/sale_report_template.xml',


    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
