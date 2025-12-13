from odoo import http
from odoo.http import request

class Profile1Controller(http.Controller):
    @http.route('/stepper_profile_1', type='http', auth='user', website=True, methods=['GET'], csrf=False)
    def profile_1(self):
        return request.render('job_portal.stepper_profile_1')

    @http.route('/stepper_profile_1/submit', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def profile_1_submit(self):
        return request.render('job_portal.stepper_profile_2')
