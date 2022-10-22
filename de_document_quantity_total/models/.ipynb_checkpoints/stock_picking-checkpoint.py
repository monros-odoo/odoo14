# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp
        
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    tot_products = fields.Integer(string='Total Products:',compute='_compute_total_products')
    tot_qty = fields.Float(string='Total Demand', compute='_compute_sum_quantity')
    tot_qty_done = fields.Float(string='Total Quantity', compute='_compute_sum_quantity')

    @api.depends('move_lines','move_lines.product_id')
    def _compute_total_products(self):
        for picking in self:
            list_of_products=[]
            for line in picking.move_lines:
                list_of_products.append(line.product_id)
            picking.tot_products = len(set(list_of_products))

    @api.depends('move_lines','move_lines.quantity_done')
    def _compute_sum_quantity(self):
        for picking in self:
            tot_qty = tot_qty_done = 0
            for line in picking.move_lines:
                tot_qty += line.product_uom_qty
                tot_qty_done += line.quantity_done
            picking.tot_qty = tot_qty
            picking.tot_qty_done = tot_qty_done