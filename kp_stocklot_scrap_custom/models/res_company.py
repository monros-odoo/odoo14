# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResComapny(models.Model):

    _inherit = "res.company"

    scrap_operation_type_id = fields.Many2one('stock.picking.type', string="Scrap Operation Type")