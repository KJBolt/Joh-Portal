from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    user_role = fields.Selection(
        selection=[
            ('jobseeker', 'Jobseeker'),
            ('employer', 'Employer'),
        ],
        string='User Role',
    )