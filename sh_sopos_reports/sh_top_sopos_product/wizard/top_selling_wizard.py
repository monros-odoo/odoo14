# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import operator

import xlwt
import base64
from io import BytesIO
import pytz
from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TopSoposSellingProductExcelExtended(models.Model):
    _name = "top.selling.sopos.excel.extended"
    _description = 'Excel Extended'

    excel_file = fields.Binary('Download report Excel')
    file_name = fields.Char('Excel File', size=64)

    def download_report(self):

        return{
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=top.selling.sopos.excel.extended&field=excel_file&download=true&id=%s&filename=%s' % (self.id, self.file_name),
            'target': 'new',
        }


class ShTspTopSellingProductWizard(models.TransientModel):
    _name = "sh.sopos.selling.product.wizard"
    _description = 'Top selling product Transient model to just filter products'

    @api.model
    def default_company_ids(self):
        is_allowed_companies = self.env.context.get(
            'allowed_company_ids', False)
        if is_allowed_companies:
            return is_allowed_companies
        return

    type = fields.Selection([
        ('basic', 'Basic'),
        ('compare', 'Compare'),
    ], string="Report Type", default="basic")

    date_from = fields.Datetime(string='From Date', required=True,default=fields.Datetime.now)
    date_to = fields.Datetime(string='To Date', required=True,
                          default=fields.Datetime.now)

    date_compare_from = fields.Datetime(string='Compare From Date',default=fields.Datetime.now)
    date_compare_to = fields.Datetime(
        string='Compare To Date', default=fields.Datetime.now)

    no_of_top_item = fields.Integer(
        string='No of Items', required=True, default=10)

    product_uom_qty = fields.Float(string="Total Qty. Sold")

    team_id = fields.Many2one("crm.team", string="Sales Channel")

    company_ids = fields.Many2many(
        'res.company', string="Companies", default=default_company_ids)
    config_ids = fields.Many2many('pos.config', string='POS Configuration')

    @api.constrains('date_from', 'date_to')
    def _check_from_to_dates(self):
        if self.filtered(lambda c: c.date_to and c.date_from > c.date_to):
            raise ValidationError(_('from date must be less than to date.'))

    @api.constrains('date_compare_from', 'date_compare_to')
    def _check_compare_from_to_dates(self):
        if self.filtered(lambda c: c.date_compare_to and c.date_compare_from and c.date_compare_from > c.date_compare_to):
            raise ValidationError(
                _('compare from date must be less than compare to date.'))

    @api.constrains('no_of_top_item')
    def _check_no_of_top_item(self):
        if self.filtered(lambda c: c.no_of_top_item <= 0):
            raise ValidationError(
                _('No of items must be positive. or not zero'))

    def filter_top_selling_product(self):
        date_start = False
        date_stop = False
        if self.date_from:
            date_start = fields.Datetime.from_string(self.date_from)
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if self.date_to:
            date_stop = fields.Datetime.from_string(self.date_to)
            # avoid a date_stop smaller than date_start
            if (date_stop < date_start):
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)
        domain = [
            ('order_id.state', 'in', ['sale', 'done']),
        ]
        if self.company_ids:
            domain.append(('order_id.company_id', 'in', self.company_ids.ids))
        if self.date_from:
            domain.append(('order_id.date_order', '>=', fields.Datetime.to_string(date_start)))
        if self.date_to:
            domain.append(('order_id.date_order', '<=', fields.Datetime.to_string(date_stop)))

        # search order line product and add into product_qty_dictionary
        search_order_lines = self.env['sale.order.line'].sudo().search(domain)
        product_qty_dic = {}
        if search_order_lines:
            for line in search_order_lines.sorted(key=lambda r: r.product_id.id):
                if product_qty_dic.get(line.product_id.id, False):
                    qty = product_qty_dic.get(line.product_id.id)
                    qty += line.product_uom_qty
                    product_qty_dic.update({line.product_id.id: qty})
                else:
                    product_qty_dic.update(
                        {line.product_id.id: line.product_uom_qty})
        date_start = False
        date_stop = False
        if self.date_from:
            date_start = fields.Datetime.from_string(self.date_from)
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if self.date_to:
            date_stop = fields.Datetime.from_string(self.date_to)
            # avoid a date_stop smaller than date_start
            if (date_stop < date_start):
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)
        domain = [
            ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
        ]
        if self.company_ids:
            domain.append(('order_id.company_id', 'in', self.company_ids.ids))
        if self.config_ids:
            session_ids = self.env['pos.session'].sudo().search(
                [('config_id', 'in', self.config_ids.ids)])
            domain.append(('order_id.session_id', 'in', session_ids.ids))
        if self.date_from:
            domain.append(('order_id.date_order', '>=', fields.Datetime.to_string(date_start)))
        if self.date_to:
            domain.append(('order_id.date_order', '<=', fields.Datetime.to_string(date_stop)))

        # search order line product and add into product_qty_dictionary
        search_pos_order_lines = self.env['pos.order.line'].sudo().search(
            domain)
        if search_pos_order_lines:
            for pos_line in search_pos_order_lines.sorted(key=lambda r: r.product_id.id):
                if product_qty_dic.get(pos_line.product_id.id, False):
                    qty = product_qty_dic.get(pos_line.product_id.id)
                    qty += pos_line.qty
                    product_qty_dic.update({pos_line.product_id.id: qty})
                else:
                    product_qty_dic.update(
                        {pos_line.product_id.id: pos_line.qty})

        # remove all the old  records before creating new one.
        top_selling_product_obj = self.env['sh.sopos.selling.product']
        search_records = top_selling_product_obj.sudo().search([])
        if search_records:
            search_records.unlink()
        if product_qty_dic:
            # sort product qty dictionary by descending order
            sorted_product_qty_list = sorted(
                product_qty_dic.items(), key=operator.itemgetter(1), reverse=True)
            counter = 0
            for tuple_item in sorted_product_qty_list:
                top_selling_product_obj.sudo().create({
                    'product_id': tuple_item[0],
                    'qty': tuple_item[1]
                })
                # only create record by user limit
                counter += 1
                if counter >= self.no_of_top_item:
                    break

    def print_top_selling_product_report(self):
        self.ensure_one()
        # we read self because we use from date and start date in our core bi logic.(in abstract model)
        data = self.read()[0]

        return self.env.ref('sh_sopos_reports.sh_sopos_selling_product_report_action').report_action([], data=data)

    def print_top_selling_product_xls_report(self):
        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        bold_center = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        left = xlwt.easyxf('align: horiz left')
        worksheet = workbook.add_sheet(
            u'Top SO and POS Selling Products', cell_overwrite_ok=True)
        if self.type == 'basic':
            worksheet.write_merge(
                0, 1, 0, 2, 'Top SO and POS Selling Products', heading_format)
        if self.type == 'compare':
            worksheet.write_merge(
                0, 1, 0, 6, 'Top SO and POS Selling Products', heading_format)
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        basic_start_date = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.date_from),
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),DEFAULT_SERVER_DATETIME_FORMAT) 
        basic_end_date = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.date_to),
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),DEFAULT_SERVER_DATETIME_FORMAT)
        compare_start_date = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.date_compare_from),
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),DEFAULT_SERVER_DATETIME_FORMAT) 
        compare_end_date = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.date_compare_to),
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),DEFAULT_SERVER_DATETIME_FORMAT)
        data = self.read()[0]
        data = dict(data or {})
        sale_order_line_obj = self.env['sale.order.line']
        pos_order_line_obj = self.env['pos.order.line']
        ##################################
        # for product from to
        date_start = False
        date_stop = False
        if data['date_from']:
            date_start = fields.Datetime.from_string(data['date_from'])
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if data['date_to']:
            date_stop = fields.Datetime.from_string(data['date_to'])
            # avoid a date_stop smaller than date_start
            if (date_stop < date_start):
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)
        domain = [
            ('order_id.state', 'in', ['sale', 'done']),
        ]
        if data.get('company_ids', False):
            domain.append(('order_id.company_id', 'in',
                           data.get('company_ids', False)))
        if data.get('date_from', False):
            domain.append(('order_id.date_order', '>=', fields.Datetime.to_string(date_start)))
        if data.get('date_to', False):
            domain.append(('order_id.date_order', '<=', fields.Datetime.to_string(date_stop)))

        if data.get('team_id'):
            team_id = data.get('team_id')
            team_id = team_id[0]
            domain.append(
                ('order_id.team_id', '=', team_id)
            )

        # search order line product and add into product_qty_dictionary
        search_order_lines = sale_order_line_obj.sudo().search(domain)

        product_total_qty_dic = {}
        if search_order_lines:
            for line in search_order_lines.sorted(key=lambda o: o.product_id.id):

                if product_total_qty_dic.get(line.product_id.name, False):
                    qty = product_total_qty_dic.get(line.product_id.name)
                    qty += line.product_uom_qty
                    product_total_qty_dic.update({line.product_id.name: qty})
                else:
                    product_total_qty_dic.update(
                        {line.product_id.name: line.product_uom_qty})

        final_product_list = []
        final_product_qty_list = []
        if product_total_qty_dic:
            # sort partner dictionary by descending order
            sorted_product_total_qty_list = sorted(
                product_total_qty_dic.items(), key=operator.itemgetter(1), reverse=True)
            counter = 0

            for tuple_item in sorted_product_total_qty_list:
                if data['product_uom_qty'] != 0 and tuple_item[1] >= data['product_uom_qty']:
                    final_product_list.append(tuple_item[0])

                elif data['product_uom_qty'] == 0:
                    final_product_list.append(tuple_item[0])

                final_product_qty_list.append(tuple_item[1])
                # only show record by user limit
                counter += 1
                if counter >= data['no_of_top_item']:
                    break
        ##################################
        # for Compare product from to
        search_order_lines = False
        compare_date_start = False
        compare_date_stop = False
        if data.get('date_compare_from', False):
            compare_date_start = fields.Datetime.from_string(data.get('date_compare_from', False))
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            compare_date_start = today.astimezone(pytz.timezone('UTC'))

        if data.get('date_compare_to', False):
            compare_date_stop = fields.Datetime.from_string(data.get('date_compare_to', False))
            # avoid a date_stop smaller than date_start
            if (compare_date_stop < compare_date_start):
                compare_date_stop = compare_date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            compare_date_stop = date_start + timedelta(days=1, seconds=-1)
        domain = [
            ('order_id.state', 'in', ['sale', 'done']),
        ]
        if data.get('company_ids', False):
            domain.append(('order_id.company_id', 'in',
                           data.get('company_ids', False)))
        if data.get('date_compare_from', False):
            domain.append(('order_id.date_order', '>=',
                           fields.Datetime.to_string(compare_date_start)))
        if data.get('date_compare_to', False):
            domain.append(('order_id.date_order', '<=',
                           fields.Datetime.to_string(compare_date_stop)))

        if data.get('team_id'):
            team_id = data.get('team_id')
            team_id = team_id[0]
            domain.append(
                ('order_id.team_id', '=', team_id)
            )

        search_order_lines = sale_order_line_obj.sudo().search(domain)

        product_total_qty_dic = {}
        if search_order_lines:
            for line in search_order_lines.sorted(key=lambda o: o.product_id.id):

                if product_total_qty_dic.get(line.product_id.name, False):
                    qty = product_total_qty_dic.get(line.product_id.name)
                    qty += line.product_uom_qty
                    product_total_qty_dic.update({line.product_id.name: qty})
                else:
                    product_total_qty_dic.update(
                        {line.product_id.name: line.product_uom_qty})

        final_compare_product_list = []
        final_compare_product_qty_list = []
        if product_total_qty_dic:
            # sort partner dictionary by descending order
            sorted_product_total_qty_list = sorted(
                product_total_qty_dic.items(), key=operator.itemgetter(1), reverse=True)
            counter = 0

            for tuple_item in sorted_product_total_qty_list:
                if data['product_uom_qty'] != 0 and tuple_item[1] >= data['product_uom_qty']:
                    final_compare_product_list.append(tuple_item[0])

                elif data['product_uom_qty'] == 0:
                    final_compare_product_list.append(tuple_item[0])

                final_compare_product_qty_list.append(tuple_item[1])
                # only show record by user limit
                counter += 1
                if counter >= data['no_of_top_item']:
                    break
        final_product_list = []
        final_product_qty_list = []
        date_start = False
        date_stop = False
        if data['date_from']:
            date_start = fields.Datetime.from_string(data['date_from'])
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if data['date_to']:
            date_stop = fields.Datetime.from_string(data['date_to'])
            # avoid a date_stop smaller than date_start
            if (date_stop < date_start):
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)
        domain = [
            ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
        ]
        if data.get('company_ids', False):
            domain.append(('order_id.company_id', 'in',
                           data.get('company_ids', False)))
        if data.get('config_ids', False):
            session_ids = self.env['pos.session'].sudo().search(
                [('config_id', 'in', data.get('config_ids', False))])
            domain.append(('order_id.session_id', 'in', session_ids.ids))
        if data.get('date_from', False):
            domain.append(('order_id.date_order', '>=', fields.Datetime.to_string(date_start)))
        if data.get('date_to', False):
            domain.append(('order_id.date_order', '<=', fields.Datetime.to_string(date_stop)))

        # search order line product and add into product_qty_dictionary
        search_pos_order_lines = pos_order_line_obj.sudo().search(domain)

        if search_pos_order_lines:
            for pos_line in search_pos_order_lines.sorted(key=lambda o: o.product_id.id):

                if product_total_qty_dic.get(pos_line.product_id.name, False):
                    qty = product_total_qty_dic.get(pos_line.product_id.name)
                    qty += pos_line.qty
                    product_total_qty_dic.update(
                        {pos_line.product_id.name: qty})
                else:
                    product_total_qty_dic.update(
                        {pos_line.product_id.name: pos_line.qty})

        if product_total_qty_dic:
            # sort partner dictionary by descending order
            sorted_product_total_qty_list = sorted(
                product_total_qty_dic.items(), key=operator.itemgetter(1), reverse=True)
            counter = 0

            for tuple_item in sorted_product_total_qty_list:
                if data['product_uom_qty'] != 0 and tuple_item[1] >= data['product_uom_qty']:
                    final_product_list.append(tuple_item[0])

                elif data['product_uom_qty'] == 0:
                    final_product_list.append(tuple_item[0])

                final_product_qty_list.append(tuple_item[1])
                # only show record by user limit
                counter += 1
                if counter >= data['no_of_top_item']:
                    break

        ##################################
        # for Compare product from to
        search_pos_order_lines = False
        compare_date_start = False
        compare_date_stop = False
        if data.get('date_compare_from', False):
            compare_date_start = fields.Datetime.from_string(data.get('date_compare_from', False))
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            compare_date_start = today.astimezone(pytz.timezone('UTC'))

        if data.get('date_compare_to', False):
            compare_date_stop = fields.Datetime.from_string(data.get('date_compare_to', False))
            # avoid a date_stop smaller than date_start
            if (compare_date_stop < compare_date_start):
                compare_date_stop = compare_date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            compare_date_stop = date_start + timedelta(days=1, seconds=-1)
        domain = [
            ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
        ]
        if data.get('company_ids', False):
            domain.append(('order_id.company_id', 'in',
                           data.get('company_ids', False)))
        if data.get('config_ids', False):
            session_ids = self.env['pos.session'].sudo().search(
                [('config_id', 'in', data.get('config_ids', False))])
            domain.append(('order_id.session_id', 'in', session_ids.ids))
        if data.get('date_compare_from', False):
            domain.append(('order_id.date_order', '>=',
                           fields.Datetime.to_string(compare_date_start)))
        if data.get('date_compare_to', False):
            domain.append(('order_id.date_order', '<=',
                           fields.Datetime.to_string(compare_date_stop)))

        search_pos_order_lines = pos_order_line_obj.sudo().search(domain)
        product_total_qty_dic = {}
        if search_pos_order_lines:
            for pos_line in search_pos_order_lines.sorted(key=lambda o: o.product_id.id):

                if product_total_qty_dic.get(pos_line.product_id.name, False):
                    qty = product_total_qty_dic.get(pos_line.product_id.name)
                    qty += pos_line.qty
                    product_total_qty_dic.update(
                        {pos_line.product_id.name: qty})
                else:
                    product_total_qty_dic.update(
                        {pos_line.product_id.name: pos_line.qty})

        if product_total_qty_dic:
            # sort partner dictionary by descending order
            sorted_product_total_qty_list = sorted(
                product_total_qty_dic.items(), key=operator.itemgetter(1), reverse=True)
            counter = 0

            for tuple_item in sorted_product_total_qty_list:
                if data['product_uom_qty'] != 0 and tuple_item[1] >= data['product_uom_qty']:
                    final_compare_product_list.append(tuple_item[0])

                elif data['product_uom_qty'] == 0:
                    final_compare_product_list.append(tuple_item[0])

                final_compare_product_qty_list.append(tuple_item[1])
                # only show record by user limit
                counter += 1
                if counter >= data['no_of_top_item']:
                    break

        # find lost and new partner here
        lost_product_list = []
        new_product_list = []
        if final_product_list and final_compare_product_list:
            for item in final_product_list:
                if item not in final_compare_product_list:
                    lost_product_list.append(item)

            for item in final_compare_product_list:
                if item not in final_product_list:
                    new_product_list.append(item)
        worksheet.write(3, 0, 'Date From: ', bold)
        worksheet.write(3, 1, basic_start_date)
        worksheet.write(4, 0, 'Date To: ', bold)
        worksheet.write(4, 1, basic_end_date)
        worksheet.col(0).width = int(25 * 260)
        worksheet.col(1).width = int(25 * 260)
        worksheet.col(2).width = int(14 * 260)
        worksheet.col(4).width = int(30 * 260)
        worksheet.col(5).width = int(25 * 260)
        worksheet.col(6).width = int(15 * 260)
        if self.type == 'compare':
            worksheet.write(3, 4, 'Compare Date From: ', bold)
            worksheet.write(3, 5, compare_start_date)
            worksheet.write(4, 4, 'Compare Date To: ', bold)
            worksheet.write(4, 5, compare_end_date)
        worksheet.write(6, 0, "#", bold)
        worksheet.write(6, 1, "Product", bold)
        worksheet.write(6, 2, "Qty Sold", bold)
        if self.type == 'compare':
            worksheet.write(6, 4, "#", bold)
            worksheet.write(6, 5, "Compare Product", bold)
            worksheet.write(6, 6, "Qty Sold", bold)
        row = 7
        if self.type == 'basic':
            no = 0
            for i in final_product_list:
                no = no + 1
                worksheet.write(row, 0, no, left)
                worksheet.write(row, 1, i, left)
                worksheet.write(row, 2, final_product_qty_list[no-1], left)
                row = row + 1
        elif self.type == 'compare':
            no = 0
            for i in final_product_list:
                no = no + 1
                worksheet.write(row, 0, no, left)
                worksheet.write(row, 1, i, left)
                worksheet.write(row, 2, final_product_qty_list[no-1], left)
                row = row + 1
            compare_row = row
            row = 7
            no = 0
            for j in final_compare_product_list:
                no = no + 1
                worksheet.write(row, 4, no, left)
                worksheet.write(row, 5, j, left)
                worksheet.write(
                    row, 6, final_compare_product_qty_list[no-1], left)
                row = row + 1
            row = compare_row + 1
            worksheet.write_merge(row, row, 0, 2, 'New Products', bold_center)
            worksheet.write_merge(row, row, 4, 6, 'Lost Products', bold_center)
            row = row + 1
            for new in new_product_list:
                worksheet.write_merge(row, row, 0, 2, new, left)
                row = row + 1
            row = compare_row + 2
            for lost in lost_product_list:
                worksheet.write_merge(row, row, 4, 6, lost, left)
                row = row + 1

        filename = ('Top SO and POS Selling Products Xls Report' + '.xls')
        fp = BytesIO()
        workbook.save(fp)

        export_id = self.env['top.selling.sopos.excel.extended'].sudo().create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename,
        })

        return{
            'type': 'ir.actions.act_window',
            'res_id': export_id.id,
            'res_model': 'top.selling.sopos.excel.extended',
            'view_mode': 'form',
            'target': 'new',
        }
