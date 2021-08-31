# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

import time

from odoo import models, api, _
from odoo.exceptions import UserError
from reportlab.graphics import barcode
from base64 import b64encode


class ReportBarcodeLabels(models.AbstractModel):
    _name = 'report.dynamic_barcode_labels.report_barcode_labels'
    _description = 'report_barcode_labels'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        config = self.env.ref('dynamic_barcode_labels.default_barcode_configuration')
        if not config:
            raise Warning(_(" Please configure barcode data from "
                            "configuration menu"))
        product_obj = self.env["product.product"]
        browse_record_list = []
        for rec in data['form']['product_ids']:
            for loop in range(0, int(rec['qty'])):
                browse_record_list.append((
                    product_obj.browse(int(rec['product_id'])),
                    rec['lot_number'],
                    rec['expir_date'],
                    rec['product_barcode']
                ))
        return {
            'doc_ids': data['form']['product_ids'],
            'doc_model': self.env['product.product'],
            'data': data,
            'docs': browse_record_list,
            'get_barcode_value': self.get_barcode_value,
            'is_humanreadable': self.is_humanreadable,
            'get_product_name': self.get_product_name,
            'time': time,
            'config': config,
            'get_barcode_string': self._get_barcode_string,
            # 'get_lot_barcode_string': self._get_lot_barcode_string,
        }

    def is_humanreadable(self, data):
        return data['form']['humanreadable'] and 1 or 0

    def get_product_name(self, product):
        return product.name

    def get_barcode_value(self, product, data):
        barcode_value = product[str(data['form']['barcode_field'])]
        return barcode_value

    def _get_barcode_string(self, product, data):
        get_lot = data['form']['product_ids']
        lot=[d['lot_number'] for d in get_lot]
        print(lot)
        if lot !=[False]:

            for g in lot:
                
                stock_lot = self.env['stock.production.lot'].search([('product_id', '=', product.id),('name', '=',g)])
                for lot in stock_lot:
                    # if lot.name == str(g):
                    barcode_value = product[str(data['form']['barcode_field'])] + '/' + str(lot.name)
                    print(barcode_value)
                    barcode_str = barcode.createBarcodeDrawing(
                        'Code128',
                        value=barcode_value,
                        format='png',
                        width=int(data['form']['barcode_height']),
                        height=int(data['form']['barcode_width']),
                        humanReadable=data['form']['humanreadable']
                    )
                    encoded_string = b64encode(barcode_str.asString('png'))
                    barcode_str = "<img style='width:" + str(data['form']['display_width']) + "px;height:" + str(
                        data['form']['display_height']) + "px'src='data:image/png;base64,{0}'>".format(
                        encoded_string.decode("utf-8"))

                    return barcode_str or ''
        if False in lot:
            barcode_value = product[str(data['form']['barcode_field'])]
            barcode_str = barcode.createBarcodeDrawing(
                data['form']['barcode_type'],
                value=barcode_value,
                format='png',
                width=int(data['form']['barcode_height']),
                height=int(data['form']['barcode_width']),
                humanReadable=data['form']['humanreadable']
            )
            encoded_string = b64encode(barcode_str.asString('png'))
            barcode_str = "<img style='width:" + str(data['form']['display_width']) + "px;height:" + str(
                data['form']['display_height']) + "px'src='data:image/png;base64,{0}'>".format(
                encoded_string.decode("utf-8"))
            return barcode_str or ''

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

class ReportBarcodeLabelsZPL(models.AbstractModel):
    _name = 'report.dynamic_barcode_labels.label_product_template_view_zpl'
    _description = 'label_product_template_view_ZPL'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        config = self.env.ref('dynamic_barcode_labels.default_barcode_configuration')
        if not config:
            raise Warning(_(" Please configure barcode data from "
                            "configuration menu"))
        product_obj = self.env["product.product"]
        browse_record_list = []
        for rec in data['form']['product_ids']:
            for loop in range(0, int(rec['qty'])):
                browse_record_list.append((
                    product_obj.browse(int(rec['product_id'])),
                    rec['lot_number'],
                    rec['expir_date'],
                    rec['company'],
                    rec['product_barcode'],
                ))
        return {
            'doc_ids': data['form']['product_ids'],
            'doc_model': self.env['product.product'],
            'data': data,
            'docs': browse_record_list,
            'get_barcode_value': self.get_barcode_value,
            'get_product_name': self.get_product_name,
            'get_barcodelot_string': self._get_barcode_string,
            'time': time,
            'config': config,

        }

    def get_product_name(self, product):
        return product.name

    def get_barcode_value(self, product, data):
        barcode_value = product[str(data['form']['barcode_field'])]
        return barcode_value

    def _get_barcode_string(self, product, data):
        get_lot = data['form']['product_ids']
        lot = [d['lot_number'] for d in get_lot]
        print(lot)
        if lot != [False]:

            for g in lot:

                stock_lot = self.env['stock.production.lot'].search([('product_id', '=', product.id), ('name', '=', g)])
                for lot in stock_lot:
                    # if lot.name == str(g):
                    if product[str(data['form']['barcode_field'])]:
                        barcode_str = product[str(data['form']['barcode_field'])] + '/' + str(lot.name)
                    else:
                        barcode_str =  str(lot.name)
                    return barcode_str or ''
        if False in lot:
            barcode_str = product[str(data['form']['barcode_field'])]
            return barcode_str or ''

