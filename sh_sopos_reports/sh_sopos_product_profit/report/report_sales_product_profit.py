# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields
import pytz
from datetime import datetime,timedelta


class SalesProductProfitAnalysis(models.AbstractModel):
    _name = 'report.sh_sopos_reports.sh_sales_product_profit_doc'
    _description = 'Sales Product Profit report abstract model'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        both_order_by_customer = []
        both_order_by_product = []
        both_order_list = []
        date_start = False
        date_stop = False
        if data['sh_start_date']:
            date_start = fields.Datetime.from_string(data['sh_start_date'])
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if data['sh_end_date']:
            date_stop = fields.Datetime.from_string(data['sh_end_date'])
            # avoid a date_stop smaller than date_start
            if (date_stop < date_start):
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)

        # Sale Customer
        if data.get('report_by') == 'customer':
            partners = False
            if data.get('sh_partner_ids', False):
                partners = self.env['res.partner'].sudo().browse(
                    data.get('sh_partner_ids', False))
            else:
                partners = self.env['res.partner'].sudo().search([])
            if partners:
                for partner_id in partners:
                    order_list = []
                    domain = [
                        ("date_order", ">=", fields.Datetime.to_string(date_start)),
                        ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                        ("partner_id", "=", partner_id.id),
                    ]
                    if data.get('company_ids', False):
                        domain.append(
                            ('company_id', 'in', data.get('company_ids', False)))
                    search_orders = self.env['sale.order'].sudo().search(
                        domain)
                    if search_orders:
                        for order in search_orders:
                            if order.order_line:
                                order_dic = {}
                                for line in order.order_line:
                                    if not line.display_type:
                                        line_dic = {
                                            'order_number': order.name,
                                            'order_date': order.date_order,
                                            'product': line.product_id.name_get()[0][1],
                                            'qty': line.product_uom_qty,
                                            'cost': line.product_id.standard_price,
                                            'sale_price': line.price_unit,
                                        }
                                        if order_dic.get(line.product_id.id, False):
                                            qty = order_dic.get(
                                                line.product_id.id)['qty']
                                            qty = qty + line.product_uom_qty
                                            line_dic.update({
                                                'qty': qty,
                                            })
                                        order_dic.update(
                                            {line.product_id.id: line_dic})
                                for key, value in order_dic.items():
                                    order_list.append(value)
                    domain1 = [
                        ("date_order", ">=", fields.Datetime.to_string(date_start)),
                        ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                        ("partner_id", "=", partner_id.id),
                        ('state', 'not in', ['draft', 'cancel'])
                    ]
                    if data.get('company_ids', False):
                        domain1.append(
                            ('company_id', 'in', data.get('company_ids', False)))
                    if data.get('sh_session_id', False):
                        domain1.append(
                            ('session_id', '=', data.get('sh_session_id', False)[0]))
                    search_orders1 = self.env['pos.order'].sudo().search(
                        domain1)
                    if search_orders1:
                        for order in search_orders1:
                            if order.lines:
                                order_dic1 = {}
                                for line in order.lines:
                                    line_dic = {
                                        'order_number': order.name,
                                        'order_date': order.date_order,
                                        'product': line.product_id.name_get()[0][1],
                                        'qty': float("{:.2f}".format(line.qty)),
                                        'cost': float("{:.2f}".format(line.product_id.standard_price)),
                                        'sale_price': float("{:.2f}".format(line.price_unit)),
                                    }
                                    if order_dic1.get(line.product_id.id, False):
                                        qty = order_dic.get(
                                            line.product_id.id)['qty']
                                        qty = qty + line.qty
                                        line_dic.update({
                                            'qty': float("{:.2f}".format(qty)),
                                        })
                                    order_dic1.update(
                                        {line.product_id.id: line_dic})
                                for key, value in order_dic1.items():
                                    order_list.append(value)
                    for item_dic in order_list:
                        both_order_by_customer.append(item_dic)

        # Sale Product
        elif data.get('report_by') == 'product':
            products = False
            if data.get('sh_product_ids', False):
                products = self.env['product.product'].sudo().browse(
                    data.get('sh_product_ids', False))
            else:
                products = self.env['product.product'].sudo().search([])
            if products:
                for product_id in products:
                    order_list = []
                    domain = [
                        ("date_order", ">=", fields.Datetime.to_string(date_start)),
                        ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                    ]
                    if data.get('company_ids', False):
                        domain.append(
                            ('company_id', 'in', data.get('company_ids', False)))
                    search_orders = self.env['sale.order'].sudo().search(
                        domain)
                    if search_orders:
                        for order in search_orders:
                            if order.order_line:
                                order_dic = {}
                                for line in order.order_line.sudo().filtered(lambda x: x.product_id.id == product_id.id):
                                    if not line.display_type:
                                        line_dic = {
                                            'order_number': order.name,
                                            'order_date': order.date_order,
                                            'customer': order.partner_id.name_get()[0][1],
                                            'qty': line.product_uom_qty,
                                            'cost': line.product_id.standard_price,
                                            'sale_price': line.price_unit,
                                        }
                                        if order_dic.get(line.product_id.id, False):
                                            qty = order_dic.get(
                                                line.product_id.id)['qty']
                                            qty = qty + line.product_uom_qty
                                            line_dic.update({
                                                'qty': qty,
                                            })
                                        order_dic.update(
                                            {line.product_id.id: line_dic})
                                for key, value in order_dic.items():
                                    order_list.append(value)
                    domain1 = [
                        ("date_order", ">=", data['sh_start_date']),
                        ("date_order", "<=", data['sh_end_date']),
                        ('state', 'not in', ['draft', 'cancel'])
                    ]
                    if data.get('company_ids', False):
                        domain1.append(
                            ('company_id', 'in', data.get('company_ids', False)))
                    if data.get('sh_session_id', False):
                        domain1.append(
                            ('session_id', '=', data.get('sh_session_id', False)[0]))
                    search_orders1 = self.env['pos.order'].sudo().search(
                        domain1)
                    if search_orders1:
                        for order in search_orders1:
                            if order.lines:
                                order_dic1 = {}
                                for line in order.lines.sudo().filtered(lambda x: x.product_id.id == product_id.id):
                                    line_dic = {
                                        'order_number': order.name,
                                        'order_date': order.date_order,
                                        'customer': order.partner_id.name_get()[0][1],
                                        'qty': float("{:.2f}".format(line.qty)),
                                        'cost': float("{:.2f}".format(line.product_id.standard_price)),
                                        'sale_price': float("{:.2f}".format(line.price_unit)),
                                    }
                                    if order_dic1.get(line.product_id.id, False):
                                        qty = order_dic1.get(
                                            line.product_id.id)['qty']
                                        qty = qty + line.qty
                                        line_dic.update({
                                            'qty': float("{:.2f}".format(qty)),
                                        })
                                    order_dic1.update(
                                        {line.product_id.id: line_dic})
                                for key, value in order_dic1.items():
                                    order_list.append(value)
                    for item_dic in order_list:
                        both_order_by_product.append(item_dic)

        # Sale Both
        elif data.get('report_by') == 'both':
            products = False
            partners = False
            if data.get('sh_product_ids', False):
                products = self.env['product.product'].sudo().browse(
                    data.get('sh_product_ids', False))
            else:
                products = self.env['product.product'].sudo().search([])
            if data.get('sh_partner_ids', False):
                partners = self.env['res.partner'].sudo().browse(
                    data.get('sh_partner_ids', False))
            else:
                partners = self.env['res.partner'].sudo().search([])
            domain = [
                ("date_order", ">=", fields.Datetime.to_string(date_start)),
                ("date_order", "<=", fields.Datetime.to_string(date_stop)),
            ]
            if data.get('company_ids', False):
                domain.append(
                    ('company_id', 'in', data.get('company_ids', False)))
            search_orders = self.env['sale.order'].sudo().search(domain)
            if search_orders:
                for order in search_orders.sudo().filtered(lambda x: x.partner_id.id in partners.ids):
                    if order.order_line:
                        order_dic = {}
                        for line in order.order_line.sudo().filtered(lambda x: x.product_id.id in products.ids):
                            if not line.display_type:
                                line_dic = {
                                    'order_number': order.name,
                                    'order_date': order.date_order,
                                    'customer': order.partner_id.name_get()[0][1],
                                    'product': line.product_id.name_get()[0][1],
                                    'qty': line.product_uom_qty,
                                    'cost': line.product_id.standard_price,
                                    'sale_price': line.price_unit,
                                }
                                if order_dic.get(line.product_id.id, False):
                                    qty = order_dic.get(line.product_id.id)['qty']
                                    qty = qty + line.product_uom_qty
                                    line_dic.update({
                                        'qty': qty,
                                    })
                                order_dic.update({line.product_id.id: line_dic})
            domain1 = [
                ("date_order", ">=", fields.Datetime.to_string(date_start)),
                ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                ('state', 'not in', ['draft', 'cancel'])
            ]
            if data.get('company_ids', False):
                domain1.append(
                    ('company_id', 'in', data.get('company_ids', False)))
            if data.get('sh_session_id', False):
                domain1.append(
                    ('session_id', '=', data.get('sh_session_id', False)[0]))
            search_orders1 = self.env['pos.order'].sudo().search(domain1)
            if search_orders1:
                for order in search_orders1.sudo().filtered(lambda x: x.partner_id.id in partners.ids):
                    if order.lines:
                        order_dic1 = {}
                        for line in order.lines.sudo().filtered(lambda x: x.product_id.id in products.ids):
                            line_dic = {
                                'order_number': order.name,
                                'order_date': order.date_order,
                                'customer': order.partner_id.name_get()[0][1],
                                'product': line.product_id.name_get()[0][1],
                                'qty': float("{:.2f}".format(line.qty)),
                                'cost': float("{:.2f}".format(line.product_id.standard_price)),
                                'sale_price': float("{:.2f}".format(line.price_unit)),
                            }
                            if order_dic1.get(line.product_id.id, False):
                                qty = order_dic1.get(line.product_id.id)['qty']
                                qty = qty + line.qty
                                line_dic.update({
                                    'qty': float("{:.2f}".format(qty)),
                                })
                            order_dic.update({line.product_id.id: line_dic})
            for key, value in order_dic.items():
                both_order_list.append(value)
        data.update({
            'date_start': data['sh_start_date'],
            'date_end': data['sh_end_date'],
            'both_order_by_customer': both_order_by_customer,
            'both_order_by_product': both_order_by_product,
            'both_order_list': both_order_list,
            'report_by': data.get('report_by'),
        })
        return data
