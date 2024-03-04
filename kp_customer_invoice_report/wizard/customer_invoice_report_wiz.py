# -*- coding: utf-8 -*-

from odoo import fields, models,api,_

class CustomerInvReportWiz(models.TransientModel):
    _name = "totalcustomer.inv.report.wiz"

    from_date = fields.Date(string="Date", default=fields.Date.today())
    to_date = fields.Date(string="Date", default=fields.Date.today())
    partner_ids = fields.Many2many('res.partner', string="Partners")
    payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')], string='Payment Status')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)

    def print_customer_inv_reports(self):
            return self.env.ref('kp_customer_invoice_report.totalcustomer_inv_total_report_tmp').report_action(self)
