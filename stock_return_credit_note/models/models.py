from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit='stock.return.request'
    credit_note=fields.Boolean()

    def create_credit_note(self):
        lines=[]
        for rec in self:
            invoice_obj = self.env['account.move']
            for l in rec.line_ids:
                dic_sales = {
                    'product_id': l.product_id.id,
                    'quantity': l.quantity or 1,
                    'price_unit': l.product_id.lst_price,

                }
                lines.append((0, 0, dic_sales))
            invoice = invoice_obj.create({
                'partner_id': self.partner_id.id,
                'move_type': 'out_refund',
                'invoice_line_ids': lines})
            if invoice:
                rec.credit_note=True

