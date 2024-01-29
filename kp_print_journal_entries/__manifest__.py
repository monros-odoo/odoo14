# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Journal Entries Customisations',
    'version': '15.0.0',
    'license': 'LGPL-3',
    'author': "Pravi/MJ",
    'category': 'General',
    'sequence': 5,
    'summary': 'Customization in jornal entries',
    'description': """Changes in journal entries""",
    'depends': ['account','base'],
    'data': ['views/account_move_view.xml',
             'reports/reports.xml',
             'reports/journal_entry_report.xml',

    ],
    'assets': {
        'web.report_assets_common': [
            'kp_print_journal_entries/static/src/scss/boxed_layout_custom.css',
        ],
    },
    'installable': True,
    'application': True,
    # 'post_init_hook': 'create_missing_journal_for_acquirers',
}
