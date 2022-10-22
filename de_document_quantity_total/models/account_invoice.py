# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class AccountMove(models.Model):
    _inherit = 'account.move'
        
    tot_products = fields.Integer(string='Total Products:',compute='_compute_total_products')
    tot_qty = fields.Float(string='Total Quantity', compute='_compute_sum_quantity')
    
    @api.depends('invoice_line_ids.product_id')
    def _compute_total_products(self):
        for invoice in self:
            list_of_product=[]
            for line in invoice.invoice_line_ids:
                list_of_product.append(line.product_id)
            invoice.tot_products = len(set(list_of_product))
    
    @api.depends('invoice_line_ids.quantity')
    def _compute_sum_quantity(self):
        for invoice in self:
            tot_qty = 0
            for line in invoice.invoice_line_ids:
                tot_qty += line.quantity
            invoice.tot_qty = tot_qty
