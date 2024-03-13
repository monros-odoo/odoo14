from odoo import _, api, fields, models

class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    product_label_name = fields.Char(string="Product Label Name")