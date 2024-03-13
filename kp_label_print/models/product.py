from odoo import _, api, fields, models
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    power = fields.Float(string="Power")
    dia = fields.Float(string="Dia")
    bc = fields.Float(string="Bc")
    qr_code = fields.Binary("QR Code", compute='_generate_qr_code')

    def _generate_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data("Product: ")
                qr.add_data(rec.name)
                qr.add_data(", Barcode: ")
                qr.add_data(rec.default_code)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.qr_code = qr_image