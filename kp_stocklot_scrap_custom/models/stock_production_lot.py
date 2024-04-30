# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError, Warning

class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    product_qty = fields.Float('Quantity', compute='_product_qty', store=True)

    def make_lotscrap_transfer(self):
        rec = self[0]
        if not rec.company_id.scrap_operation_type_id:
            raise ValidationError("Please select Scrap Operation Type in Company.")
        scrap_picking_type_id = rec.company_id.scrap_operation_type_id
        if scrap_picking_type_id and not scrap_picking_type_id.default_location_src_id:
            raise ValidationError("Please select source location in Scrap opeartion type")
        if scrap_picking_type_id and not scrap_picking_type_id.default_location_dest_id:
            raise ValidationError("Please select destination location in Scrap opeartion type")
        picking_vals = {'picking_type_id': scrap_picking_type_id.id,
                        'is_scrap_transfer': True,
                        'location_id': scrap_picking_type_id.default_location_src_id.id,
                        'location_dest_id': scrap_picking_type_id.default_location_dest_id.id,
                        'state': 'draft',
                        'move_ids_without_package': [(0, 0, {'product_id': lot.product_id.id if lot.product_id else False,
                                                             'lot_id': lot.id,
                                                             'product_uom_qty': lot.product_qty,
                                                             'name': lot.product_id.partner_ref if lot.product_id else False,
                                                             'product_uom': lot.product_id.uom_id.id if lot.product_id and lot.product_id.uom_id else False,
                                                             }) for lot in self]}

        stock_picking = self.env['stock.picking'].sudo().create(picking_vals)
        print(stock_picking)
        if stock_picking and len(self) == 1:
            title = _("Successfully!")
            message = "Transfer Created Successfully - " + stock_picking.name
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'sticky': False,
                }
            }

            # return {
            #     'effect': {
            #         'fadeout': 'slow',
            #         'message': message,
            #
            #     }
            # }

