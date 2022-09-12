# -*- coding: utf-8 -*-
{
    'name': "Invoice Report",

    'summary': """
       Invoice Report""",

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account',],

    # always loaded
    'data': [
        'report/report.xml',
        # 'report/invoice_header_footer.xml',
        'views/invoice_report.xml',
    ],

}
