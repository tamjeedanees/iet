from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    minimum_margin = fields.Float(string="Minimum Margin",
                                  config_parameter='gallery_design.minimum_margin',
                                  help="The field is to define the minimum margin added into sales price of product.")
    maximum_margin = fields.Float(string="Maximum Margin",
                                  config_parameter='gallery_design.maximum_margin',
                                  help="The field is to define the maximum margin added into sales price of product.")
