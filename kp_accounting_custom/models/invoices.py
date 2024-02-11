from odoo import models, fields


class InvoiceReport(models.Model):
    _inherit = 'account.move'

    description = fields.Char(string='Description')
