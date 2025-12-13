from odoo import http
from odoo.http import request

class Profile1Controller(http.Controller):
    @http.route('/stepper_profile', type='http', auth='user', website=True, methods=['GET'], csrf=False)
    def profile_complete(self):
        return request.render('job_portal.stepper_profile')

    @http.route('/stepper_profile/submit', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def profile_submit(self, **post):
        return request.render('job_portal.stepper_profile_1')
