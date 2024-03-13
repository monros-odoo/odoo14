from odoo import _, api, fields, models
from odoo.tools.image import image_data_uri
from datetime import datetime

class StockProductionLotInherit(models.Model):
    _inherit = "stock.production.lot"


    def print_new_label_report(self):
        return self.env.ref('kp_label_print.report_lot_stock_product_report').report_action(self)

