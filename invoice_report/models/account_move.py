from odoo import models, fields, api

class AccountInvoiceInhr(models.Model):
    _inherit = 'account.move'

    def get_picking_name(self):
        name =''
        if self.invoice_origin:
                so = self.env['sale.order'].search([('name', '=', self.invoice_origin)])
                if so:
                     name = so.warehouse_id.name

        return name
