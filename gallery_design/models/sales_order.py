from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def product_sales_margin_restrict(self):
        min_margin = self.env['ir.config_parameter'].sudo().get_param('gallery_design.minimum_margin')
        max_margin = self.env['ir.config_parameter'].sudo().get_param('gallery_design.maximum_margin')
        for rec in self:
            for product in rec.order_line:
                if product and product.product_id.standard_price and product.product_id.list_price:
                    cost = product.product_id.standard_price
                    if min_margin:
                        min_value = ((cost / 100) * float(min_margin)) + cost
                    if max_margin:
                        max_value = (cost / 100) * float(max_margin) + cost
                    if product.price_unit < min_value or product.price_unit > max_value:
                        raise UserError(_('Unit price should be in between the range of margins.'))