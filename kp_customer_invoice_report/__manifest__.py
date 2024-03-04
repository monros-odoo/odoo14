# -*- coding: utf-8 -*-
{
    "name": "Customer Invoice Report",
    "version": "14.0.1.0.2",
    "category": "Accounting/Accounting",
    "depends": ['account','web'],
    "data": [
        'security/ir.model.access.csv',
        'report/customer_invoice_total_report.xml',
        'report/report.xml',
        'wizard/customer_inv_report_wiz.xml',
    ],
    "application": False,
    "installable": True,
    'auto_install': False,
}
