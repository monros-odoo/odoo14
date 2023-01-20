# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Faslu Rahman(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': ' Discount on Total Amount',
    'version': '14.0.1.1.0',
    'category': 'Sales Management',
    'summary': "Discount on Total ",
    'author': 'Ahmed Hussein',
    'website': '',
    'description': """

 Discount for Total Amount

""",
    'depends': ['sale',
                'account', 'delivery'
                ],
    'data': [
        'views/sale_view.xml',
        'views/account_invoice_view.xml',
        # 'views/invoice_report.xml',
        'views/sale_order_report.xml',
        'views/res_config_view.xml',

    ],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}