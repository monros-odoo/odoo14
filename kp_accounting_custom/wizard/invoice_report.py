from odoo import fields, models, api
from odoo.exceptions import ValidationError



class AccountingInvoiceReport(models.TransientModel):
    _name = 'invoice.report'

    start_date = fields.Date(required=True, string='From Date')
    end_date = fields.Date(required=True, string='End Date')
    partner_id = fields.Many2one('res.partner', 'Customer', required=True)

    def generate_invoice_report(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be greater than From date.")

        invoice_details = self.get_invoice_report_details()

        if not invoice_details:
            raise ValidationError("No Records found!.")

        return self.env.ref('kp_accounting_custom.invoice_report').report_action(self)

    @api.model
    def get_invoice_report_details(self):
        invoice_lines = self.env['account.move'].search([
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'in_invoice']),
        ])

        return invoice_lines

    @api.model
    def get_payment_status_name(self, item):
        return dict(item._fields['payment_state'].selection).get(item.payment_state)





