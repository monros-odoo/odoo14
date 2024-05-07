# -*- coding: utf-8 -*-

from odoo import fields, models, api
import werkzeug.urls


class ResCompany(models.Model):
    _inherit = "res.company"

    sale_discount_product_id = fields.Many2one('product.product', string='Sale Discount Product')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_discount_product_id = fields.Many2one('product.product', related='company_id.sale_discount_product_id', string='Sale Discount Product', readonly=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: