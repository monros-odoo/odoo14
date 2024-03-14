# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: SAYOOJ A O (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import models, fields ,api,_
from odoo.tools.float_utils import float_round


class PickingInvoiceWizard(models.TransientModel):
    _name = 'picking.invoice.wizard'
    _description = "Create Invoice from picking"

    def picking_multi_invoice(self):
        active_ids = self._context.get('active_ids')
        picking_ids = self.env['stock.picking'].browse(active_ids)
        picking_id = picking_ids.filtered(lambda x: x.state == 'done' and x.invoice_count == 0)
        for picking in picking_id:
            if picking.picking_type_id.code == 'incoming' and not picking.is_return:
                picking.create_bill()
            if picking.picking_type_id.code == 'outgoing' and not picking.is_return:
                picking.create_invoice()
            if picking.picking_type_id.code == 'incoming' and picking.is_return:
                picking.create_vendor_credit()
            if picking.picking_type_id.code == 'outgoing' and picking.is_return:
                picking.create_customer_credit()


class StockReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    lot_id = fields.Many2one('stock.production.lot', string='Lot/Serial Number', help="Lot/Serial number concerned by the ticket", domain="[('product_id', '=', product_id)]")


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _prepare_move_default_values(self, return_line, new_picking):
        vals = super(StockReturnPicking, self)._prepare_move_default_values(return_line, new_picking)
        vals['lot_id'] = return_line.lot_id.id
        return vals

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move):
        quantity = stock_move.product_qty
        for move in stock_move.move_dest_ids:
            if move.origin_returned_move_id and move.origin_returned_move_id != stock_move:
                continue
            if move.state in ('partially_available', 'assigned'):
                quantity -= sum(move.move_line_ids.mapped('product_qty'))
            elif move.state in ('done'):
                quantity -= move.product_qty
        quantity = float_round(quantity, precision_rounding=stock_move.product_id.uom_id.rounding)
        return {
            'product_id': stock_move.product_id.id,
            'lot_id': stock_move.lot_id.id,
            'quantity': quantity,
            'move_id': stock_move.id,
            'uom_id': stock_move.product_id.uom_id.id,
        }

