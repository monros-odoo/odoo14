# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _


class AccountMoveline(models.Model):
    _inherit = 'account.move.line'
    total_before_discount = fields.Float(compute='compute_total_before_discount', string='Subtotal')

    @api.depends('price_unit', 'quantity')
    def compute_total_before_discount(self):
        for rec in self:

            rec.total_before_discount= rec.price_unit * rec.quantity


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_before_discount = fields.Float(compute='compute_total_before_discount', string='Subtotal')

    @api.depends('invoice_line_ids.price_unit','invoice_line_ids.quantity')
    def compute_total_before_discount(self):
        for rec in self:

            total_before_discount = 0.0
            for line in self.invoice_line_ids:
                total_before_discount += line.price_unit * line.quantity

            rec.total_before_discount = total_before_discount

