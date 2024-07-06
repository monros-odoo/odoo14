
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Float('Price Discount', compute='get_discount_amount', store=True)
    price_after_disc = fields.Float('Price AD', compute='get_price_after_disc', store=True)
    total_discount = fields.Float('Total Discount', compute='get_tot_discount_amount', store=True)

    @api.depends('discount')
    def get_discount_amount(self):
        for rec in self:
            rec.discount_amount = (rec.discount * rec.price_unit) / 100

    @api.depends('discount_amount')
    def get_price_after_disc(self):
        for rec in self:
            rec.price_after_disc = rec.price_unit - rec.discount_amount

    @api.depends('quantity','discount_amount')
    def get_tot_discount_amount(self):
        for rec in self:
            rec.total_discount = rec.quantity * rec.discount_amount



class AccountMove(models.Model):
    _inherit = 'account.move'


    total_qty = fields.Float('Total Qty', compute='get_tot_tot_qty', store=True)
    total_discount = fields.Float('Total Discount', compute='get_tot_discount_amount', store=True)
    total_before_discount = fields.Float('Total Before Discount', compute='get_tot_before_discount_amount', store=True)
    amount_text = fields.Char(compute='get_total_amount_text', store=True)

    @api.depends('amount_total_signed')
    def get_total_amount_text(self):
        for rec in self:
            rec.amount_text = rec.currency_id.amount_to_text(rec.amount_total_signed)


    @api.depends('invoice_line_ids','invoice_line_ids.total_discount')
    def get_tot_discount_amount(self):
        for rec in self:
            tot = 0.0
            for line in rec.invoice_line_ids:
                tot += line.total_discount
            rec.total_discount = tot


    @api.depends('invoice_line_ids','invoice_line_ids.quantity')
    def get_tot_tot_qty(self):
        for rec in self:
            tot = 0.0
            for line in rec.invoice_line_ids:
                tot += line.quantity
            rec.total_qty = tot


    @api.depends('amount_untaxed_signed','total_discount')
    def get_tot_before_discount_amount(self):
        for rec in self:
            rec.total_before_discount = rec.amount_untaxed_signed + rec.total_discount


