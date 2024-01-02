from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('list_price')
    def sales_margin_restrict(self):
        min_margin = self.env['ir.config_parameter'].sudo().get_param('gallery_design.minimum_margin')
        max_margin = self.env['ir.config_parameter'].sudo().get_param('gallery_design.maximum_margin')
        for rec in self:
            cost = rec.standard_price
            if min_margin:
                min_value = ((cost / 100) * float(min_margin)) + cost
            if max_margin:
                max_value = (cost / 100) * float(max_margin) + cost
            if rec.list_price < min_value or rec.list_price > max_value:
                raise UserError(_("Sales price should be in between the range of margins."))