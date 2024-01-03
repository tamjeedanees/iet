from odoo import models, fields, api, _


class StockValuationAnalysis(models.TransientModel):
    _name = "stock.valuation.layer.report"
    _description = ""


    item_number = fields.Char(string="Item Number")
    qty_beginning = fields.Float(string="Quantity (At the beginning)")
    val_beginning = fields.Float(string="Value (At the beginning)")
    qty_receipt = fields.Float(string="Quantity (Receipt)")
    val_receipt = fields.Float(string="Value (Receipt)")
    qty_issue = fields.Float(string="Quantity (Issue)")
    val_issue = fields.Float(string="Value (Issue)")
    qty_end = fields.Float(string="Quantity (At the end)")
    val_end = fields.Float(string="Value (At the end)")
