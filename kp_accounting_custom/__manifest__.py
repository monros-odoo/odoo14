# -*- coding: utf-8 -*-
{
    'name': "KP Accounting Custom",

    'summary': """ KP Accounting Custom """,

    'description': """    """,
    'author': "JITHIN/KP",
    'website': "https://www.kuwaitprotocol.com/",
    'version': '14.0.0',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/invoice_report_view.xml',
        'wizard/invoice_report.xml',
        'views/invoices.xml',
    ],
    'assets': {},
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}