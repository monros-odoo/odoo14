# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            total = 0.0
            if order.discount_types == 'fixed':
                self.amount_discount = order.acs_discount_amount
            if order.discount_types == 'percentage':
                for line in order.order_line:
                    total += line.price_subtotal
                amount = (total * order.discount_percentage)/100
                self.amount_discount = amount
            order.update({
                'amount_untaxed': amount_untaxed + self.amount_discount,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

    global_discount = fields.Boolean("Add Global Discount", readonly=True, states={'draft': [('readonly', False)]},)
    discount_types = fields.Selection([('fixed','Fixed'),('percentage','Percentage')],
        "Discount Type", readonly=True, states={'draft': [('readonly', False)]}, default='fixed')
    acs_discount_amount = fields.Float("Discount Amount", readonly=True, states={'draft': [('readonly', False)]},)
    discount_percentage = fields.Float("Discount Percentage", readonly=True, states={'draft': [('readonly', False)]},)
    total_discount_amount = fields.Float("Discount Amount", store=True)
    amount_untaxed_dis = fields.Monetary(string='Untaxed Amount', store=True,
                                         compute='_compute_amount_untaxed_dis',
                                         track_visibility='always')
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always')
    amount_discount = fields.Monetary(string='Discount', store=True, track_visibility='always')

    @api.depends('total_discount_amount', 'amount_untaxed')
    def _compute_amount_untaxed_dis(self):
        for rec in self:
            rec.amount_untaxed_dis = rec.amount_untaxed + rec.total_discount_amount

    def _discount_unset(self):
        if self.env.user.company_id.sale_discount_product_id:
            self.env['sale.order.line'].search([('order_id', 'in', self.ids), ('product_id', '=', self.env.user.company_id.sale_discount_product_id.id)]).unlink()

    def create_discount(self):
        Line = self.env['sale.order.line']

        product_id = self.env.user.company_id.sale_discount_product_id
        if not product_id:
            raise UserError(_('Please set Sale Discount product in General Settings first.'))

        # Remove Discount line first
        self._discount_unset()

        for order in self:
            amount = 0.0
            total = 0.0
            if order.discount_types == 'fixed':
                amount = order.acs_discount_amount
                self.amount_discount = order.acs_discount_amount
            if order.discount_types == 'percentage':
                for line in order.order_line:
                    total += line.price_subtotal
                amount = (total * order.discount_percentage)/100
                self.amount_discount = amount

            # Create the Sale line
            Line.create({
                'name': product_id.name,
                'price_unit': -amount,
                'product_uom_qty': 1.0,
                'discount': 0.0,
                'product_uom': product_id.uom_id.id,
                'product_id': product_id.id,
                'order_id': order.id,
                'sequence': 100,
            })
        return True

    def _prepare_invoice(self, ):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'total_discount': self.amount_discount,
            'total_before_discount': self.amount_untaxed

        })
        return invoice_vals
