# -*- coding: utf-8 -*-

from odoo import api, models,fields


class TotalCustomerInvoice(models.AbstractModel):
    _name = 'report.kp_customer_invoice_report.totalcustomer_inv_report'
    _description = 'Total Customer Invoice Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_wiz = self.env['totalcustomer.inv.report.wiz'].browse(docids)
        domain = [('invoice_date', '>=', report_wiz.from_date), ('invoice_date', '<=', report_wiz.to_date), ('move_type', '=', 'out_invoice')]
        if report_wiz.partner_ids:
            domain += [('partner_id', 'in', report_wiz.partner_ids.ids)]
        if report_wiz.payment_state:
            domain += [('payment_state', '=', report_wiz.payment_state)]
        account_move = self.env['account.move'].sudo().search(domain)
        invoice_list = []
        if len(account_move) > 1:
            move_query = """
                            SELECT sum(amount_total) AS Amount, Count(id) AS count , acc_mv.partner_id As Customer FROM account_move AS acc_mv
                           WHERE acc_mv.id IN %s group by acc_mv.partner_id """ % (tuple(account_move.ids),)
            self.env.cr.execute(move_query)
            customer_invoices = self.env.cr.dictfetchall()

            for customer_invoice in customer_invoices:
                customer = self.env['res.partner'].sudo().browse(customer_invoice['customer'])
                vals = {'Partner': customer.name if customer else False,
                        'Amount': customer_invoice['amount'],
                        'Inv Count': customer_invoice['count']}
                invoice_list.append(vals)
        if len(account_move) == 1:
            move_query = """
                            SELECT sum(amount_total) AS Amount, Count(id) AS count , acc_mv.partner_id As Customer FROM account_move AS acc_mv
                           WHERE acc_mv.id = %s group by acc_mv.partner_id """ % (account_move.id)
            self.env.cr.execute(move_query)
            customer_invoices = self.env.cr.dictfetchall()

            for customer_invoice in customer_invoices:
                customer = self.env['res.partner'].sudo().browse(customer_invoice['customer'])
                vals = {'Partner': customer.name if customer else False,
                        'Amount': customer_invoice['amount'],
                        'Inv Count': customer_invoice['count']}
                invoice_list.append(vals)
        return {
            'doc_ids': docids,
            'doc_model': 'totalcustomer.inv.report.wiz',
            'docs': report_wiz,
            'invoice_lists': invoice_list,
        }
