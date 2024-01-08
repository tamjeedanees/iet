from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('list_price')
    def sales_margin_restrict(self):
        min_margin = self.env['ir.config_parameter'].sudo().get_param('iet_gallery_design.minimum_margin')
        max_margin = self.env['ir.config_parameter'].sudo().get_param('iet_gallery_design.maximum_margin')
        for rec in self:
            if rec.standard_price:
                cost = rec.standard_price
                if not min_margin or not max_margin:
                    raise UserError(_("Set min and max margin value in config settings."))
                if min_margin:
                    min_value = cost * float(min_margin)
                if max_margin:
                    max_value = cost * float(max_margin)
                if rec.list_price < min_value or rec.list_price > max_value:
                    raise UserError(_("Sales price should be in between the range of margins."))