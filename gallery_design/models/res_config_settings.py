from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    minimum_margin = fields.Float(string="Minimum Margin",
                                  config_parameter='gallery_design.minimum_margin',
                                  help="The field is to define the minimum margin added into sales price of product.")
    maximum_margin = fields.Float(string="Maximum Margin",
                                  config_parameter='gallery_design.maximum_margin',
                                  help="The field is to define the maximum margin added into sales price of product.")


    @api.onchange('minimum_margin', 'maximum_margin')
    def restrict_margin_settings(self):
        for rec in self:
            min = rec.minimum_margin < 0 or rec.maximum_margin < 0
            max = rec.minimum_margin > 100.0 or rec.maximum_margin > 100.0
            if min or max:
                raise UserError(_("Minimum or Maximum margin should be in range between 0 - 100."))
