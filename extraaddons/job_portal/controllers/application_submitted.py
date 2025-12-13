from odoo import http
from odoo.http import request

class ApplicationSubmitted(http.Controller):
    @http.route('/application-submitted', type='http', auth='public', website=True, method=['GET'], csrf=False)
    def application_submitted(self):
        return request.render('job_portal.application_submitted')