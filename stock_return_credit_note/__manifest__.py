# -*- coding: utf-8 -*-
{
    'name': "Stock Return Credit Note",

    'summary': """
    Stock Return Credit Note
        """,


    'depends': ['base','stock','account','stock_return_request'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/wizard_credit_note.xml',

    ],

}
