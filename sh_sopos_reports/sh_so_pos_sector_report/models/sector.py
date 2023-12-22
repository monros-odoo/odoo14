# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, exceptions, _
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError

class Sector(models.Model):
    _name = 'sh.sale.pos.sector'
    _order = 'sequence, id'
    
    name = fields.Char(string = "Name" , required = True)
    from_time = fields.Float(string = "From",required=True)
    to_time = fields.Float(string = "To",required=True)
    sequence = fields.Integer("Sequence")
    