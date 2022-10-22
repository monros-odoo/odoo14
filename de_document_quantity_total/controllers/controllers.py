# -*- coding: utf-8 -*-
# from odoo import http


# class DeDocumentQuantityTotal(http.Controller):
#     @http.route('/de_document_quantity_total/de_document_quantity_total/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_document_quantity_total/de_document_quantity_total/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_document_quantity_total.listing', {
#             'root': '/de_document_quantity_total/de_document_quantity_total',
#             'objects': http.request.env['de_document_quantity_total.de_document_quantity_total'].search([]),
#         })

#     @http.route('/de_document_quantity_total/de_document_quantity_total/objects/<model("de_document_quantity_total.de_document_quantity_total"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_document_quantity_total.object', {
#             'object': obj
#         })
