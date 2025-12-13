from odoo import http
from odoo.http import request

class Pricing(http.Controller):
    @http.route('/pricing', type='http', auth='public', website=True)
    def pricing(self):
        return request.render('job_portal.pricing')