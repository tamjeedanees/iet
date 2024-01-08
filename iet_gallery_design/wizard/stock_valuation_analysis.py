from odoo import models, fields, api, _


class StockValuationAnalysis(models.TransientModel):
    _name = "stock.valuation.analysis"
    _description = ""


    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    product_id = fields.Many2many('product.product', 'stock_valuation_product_rel', 'stock_valuation_wizard_id', 'product_id', string="Products")
    product_category_id = fields.Many2many('product.category', 'stock_valuation_product_cat_rel', 'stock_valuation_wizard_id', 'category_id', string="Product Categories")


    def quantity_at_the_beginning(self, product_id):
        stock_valuation_layer = self.env['stock.valuation.layer']
        domain = [('create_date', '<', self.start_date), ('product_id', '=', product_id.id)]
        qty_beginning = 0.0
        for rec in self:
            layer_data = stock_valuation_layer.search(domain)
            qty_beginning = sum([x.quantity for x in layer_data])
        
        return qty_beginning

    def value_at_the_beginning(self, product_id):
        stock_valuation_layer = self.env['stock.valuation.layer']
        domain = [('create_date', '<', self.start_date), ('product_id', '=', product_id.id)]
        qty_value = 0.0
        for rec in self:
            layer_data = stock_valuation_layer.search(domain)
            qty_value = sum([x.value for x in layer_data])
        
        return qty_value

    def quantity_receipt(self, layers_data):
        incoming_data = layers_data.filtered(lambda layer: layer.stock_move_id.picking_id.picking_type_code == 'incoming')
        return sum([x.quantity for x in incoming_data]) if incoming_data else 0.0

    def value_receipt(self, layers_data):
        incoming_data = layers_data.filtered(lambda layer: layer.stock_move_id.picking_id.picking_type_code == 'incoming')
        return sum([x.value for x in incoming_data]) if incoming_data else 0.0

    def quantity_issue(self, layers_data):
        outgoing_data = layers_data.filtered(lambda layer: layer.stock_move_id.picking_id.picking_type_code == 'outgoing')
        return sum([x.quantity for x in outgoing_data]) if outgoing_data else 0.0

    def value_issue(self, layers_data):
        outgoing_data = layers_data.filtered(lambda layer: layer.stock_move_id.picking_id.picking_type_code == 'outgoing')
        return sum([x.value for x in outgoing_data]) if outgoing_data else 0.0

    def get_data_stock_valuation_layer(self):
        stock_valuation_layer = self.env['stock.valuation.layer']
        report_data = []
        domain = []
        for layer in self:
            domain = [('create_date','>=',self.start_date),('create_date','<=',self.end_date)]
            if layer.product_id:
                domain.append(('product_id', 'in', [x.id for x in self.product_id]))
            if layer.product_category_id:
                domain.append(('product_id.categ_id', 'in', [x.id for x in self.product_category_id]))
            stock_layers = stock_valuation_layer.search(domain)
            product_ids = stock_layers.mapped('product_id')
            for product_id in product_ids:
                layers_data = stock_layers.filtered(lambda layer: layer.product_id == product_id)
                qty_beginning, val_beginning = self.quantity_at_the_beginning(product_id), self.value_at_the_beginning(product_id)
                qty_receipt, val_receipt = self.quantity_receipt(layers_data), self.value_receipt(layers_data)
                qty_issue, val_issue = self.quantity_issue(layers_data), self.value_issue(layers_data)
                report_data.append({
                    "item_number": product_id.default_code,
                    "qty_beginning": qty_beginning,
                    "val_beginning": val_beginning,
                    "qty_receipt": qty_receipt,
                    "val_receipt": val_receipt,
                    "qty_issue": qty_issue,
                    "val_issue": val_issue,
                    "qty_end": (qty_beginning + qty_receipt) - abs(qty_issue),
                    "val_end": (val_beginning + val_receipt) - abs(val_issue)
                })

        return report_data

    def view_data(self):
        view_mode = 'tree'
        tree_view_id = self.env.ref('iet_gallery_design.stock_valuation_layer_report_tree').id

        # Remove all existing records from 'stock.valuation.layer.report'
        existing_records = self.env['stock.valuation.layer.report'].sudo().search([])
        existing_records.unlink()

        # Create new records
        stock_valuation_analysis_report = self.get_data_stock_valuation_layer()
        for data in stock_valuation_analysis_report:
            self.env['stock.valuation.layer.report'].sudo().create(data)

        return {
            'name': 'Stock Valuation Analysis Report',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.valuation.layer.report',
            'view_mode': view_mode,
            'views': [(tree_view_id, 'tree')],
            'res_id': False,
            'target': 'self',
        }
