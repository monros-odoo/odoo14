from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    total_discount_amount = fields.Float("Discount Amount", store=True)
    amount_untaxed_dis = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_compute_amount_untaxed_dis',
                                     track_visibility='always')

    @api.depends('total_discount_amount','amount_untaxed')
    def _compute_amount_untaxed_dis(self):
        for rec in self:
            rec.amount_untaxed_dis = rec.amount_untaxed-(rec.total_discount_amount)
