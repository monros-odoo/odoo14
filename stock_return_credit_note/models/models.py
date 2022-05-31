from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class accountmove(models.Model):
    _inherit='account.move'

    stock_return_id=fields.Many2one('stock.return.request')

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
                'stock_return_id':rec.id,
                'invoice_line_ids': lines})
            if invoice:
                rec.credit_note=True

    def compute_related_credit(self):
        for line in self:
            line.credit_count = self.env['account.move'].search_count([('stock_return_id', '=', line.id)])

    credit_count = fields.Integer(compute='compute_related_credit')

    def get_credit_view(self):
        self.ensure_one()
        domain = [
            ('stock_return_id', '=', self.id)
        ]
        return {
            'name': _('Related Credit '),
            'domain': domain,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': "{'create':False}"

        }


