from odoo import http
from odoo.http import request

class StepperProfile2(http.Controller):
    @http.route('/stepper_profile_2', type='http', auth='user', website=True)
    def stepper_profile_2(self):
        return request.render('job_portal.stepper_profile_2')

    @http.route('/stepper_profile_2/submit', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def stepper_profile_2_submit(self):
        return request.render('job_portal.stepper_profile_2')
