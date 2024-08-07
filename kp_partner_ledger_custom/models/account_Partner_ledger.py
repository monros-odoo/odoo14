from odoo import models,fields,api,_
from odoo.tools.misc import format_date


class PartnerLedger(models.AbstractModel):
    _name = "account.partner.ledger"
    _inherit = ["account.partner.ledger","account.report"]

    @api.model
    def _get_templates(self):
        print(self.env.context,'self.env.context')
        templates = super(PartnerLedger, self)._get_templates()
        templates['line_template'] = 'account_reports.line_template_partner_ledger_report'
        templates['main_template'] = 'account_reports.main_template_with_filter_input_partner'
        if self._context.get('print_mode'):
            templates['main_table_header_template'] = 'kp_partner_ledger_custom.main_table_header_partner_ledger'
        return templates

    @api.model
    def _get_report_line_partner(self, options, partner, initial_balance, debit, credit, balance):
        print(self.env.context, 'self.env.context')
        company_currency = self.env.company.currency_id
        unfold_all = self._context.get('print_mode') and not options.get('unfolded_lines')
        if self._context.get('print_mode') and self._get_report_name() == 'Partner Ledger' and not self.env.context.get('no_format'):
            columns = [
                # {'name': self.format_value(initial_balance), 'class': 'number'},
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
            ]
        else:
            columns = [
                {'name': self.format_value(initial_balance), 'class': 'number'},
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
            ]
            if self.user_has_groups('base.group_multi_currency'):
                columns.append({'name': ''})
        columns.append({'name': self.format_value(balance), 'class': 'number'})

        if self._context.get('print_mode') and self._get_report_name() == 'Partner Ledger' and not self.env.context.get('no_format'):
            return {
                'id': 'partner_%s' % (partner.id if partner else 0),
                'partner_id': partner.id if partner else None,
                'name': partner is not None and (partner.name or '')[:128] or _('Unknown Partner'),
                'columns': columns,
                'level': 2,
                'trust': partner.trust if partner else None,
                'unfoldable': not company_currency.is_zero(debit) or not company_currency.is_zero(credit),
                'unfolded': 'partner_%s' % (partner.id if partner else 0) in options['unfolded_lines'] or unfold_all,
                'colspan': 2,
            }
        else:
            return {
                'id': 'partner_%s' % (partner.id if partner else 0),
                'partner_id': partner.id if partner else None,
                'name': partner is not None and (partner.name or '')[:128] or _('Unknown Partner'),
                'columns': columns,
                'level': 2,
                'trust': partner.trust if partner else None,
                'unfoldable': not company_currency.is_zero(debit) or not company_currency.is_zero(credit),
                'unfolded': 'partner_%s' % (partner.id if partner else 0) in options['unfolded_lines'] or unfold_all,
                'colspan': 6,
            }

    @api.model
    def _get_report_line_move_line(self, options, partner, aml, cumulated_init_balance, cumulated_balance):
        print(self.env.context, 'self.env.context')
        if aml['payment_id']:
            caret_type = 'account.payment'
        else:
            caret_type = 'account.move'

        line_name = self._format_aml_name(aml['name'], aml['ref'], aml['move_name'])
        print('line_name', line_name)
        if self.env.context.get('print_mode', False) and self._get_report_name() == 'Partner Ledger' and not self.env.context.get('no_format'):
            columns = [
                # {'name': aml['journal_code']},
                # {'name': aml['account_code']},
                {'name': line_name, 'title': line_name, 'class': 'o_account_report_line_ellipsis'},
                # {'name': self.format_report_date(aml['date_maturity']) or '', 'class': 'date'},
                # {'name': aml['matching_number'] or ''},
                # {'name': self.format_value(cumulated_init_balance), 'class': 'number'},
                {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
                {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
            ]
        else:
            columns = [
                {'name': aml['journal_code']},
                {'name': aml['account_code']},
                {'name': line_name, 'title': line_name, 'class': 'o_account_report_line_ellipsis'},
                {'name': self.format_report_date(aml['date_maturity']) or '', 'class': 'date'},
                {'name': aml['matching_number'] or ''},
                {'name': self.format_value(cumulated_init_balance), 'class': 'number'},
                {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
                {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
            ]
            if self.user_has_groups('base.group_multi_currency'):
                if aml['currency_id']:
                    currency = self.env['res.currency'].browse(aml['currency_id'])
                    formatted_amount = self.format_value(aml['amount_currency'], currency=currency, blank_if_zero=True)
                    columns.append({'name': formatted_amount, 'class': 'number'})
                else:
                    columns.append({'name': ''})
        columns.append({'name': self.format_value(cumulated_balance), 'class': 'number'})
        return {
            'id': aml['id'],
            'parent_id': 'partner_%s' % (partner.id if partner else 0),
            'name': format_date(self.env, aml['date']),
            'class': 'text' + aml.get('class', ''),  # do not format as date to prevent text centering
            'columns': columns,
            'caret_options': caret_type,
            'level': 2,
        }



    @api.model
    def _get_report_line_total(self, options, initial_balance, debit, credit, balance):
        print(self.env.context, 'self.env.context')
        if self.env.context.get('print_mode', False) and self._get_report_name() == 'Partner Ledger' and not self.env.context.get('no_format'):
            columns = [
                # {'name': self.format_value(initial_balance), 'class': 'number'},
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
            ]
        else:
            columns = [
                {'name': self.format_value(initial_balance), 'class': 'number'},
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
            ]
            if self.user_has_groups('base.group_multi_currency'):
                columns.append({'name': ''})
        columns.append({'name': self.format_value(balance), 'class': 'number'})
        if self.env.context.get('print_mode', False) and self._get_report_name() == 'Partner Ledger' and not self.env.context.get('no_format'):
            return {
                'id': 'partner_ledger_total_%s' % self.env.company.id,
                'name': _('Total'),
                'class': 'total',
                'level': 1,
                'columns': columns,
                'colspan': 2,
            }
        else:
            return {
                'id': 'partner_ledger_total_%s' % self.env.company.id,
                'name': _('Total'),
                'class': 'total',
                'level': 1,
                'columns': columns,
                'colspan': 6,
            }