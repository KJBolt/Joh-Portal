from odoo import http
from odoo.http import request

class Home(http.Controller):
    @http.route('/home', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def index(self):
        return request.render('job_portal.home')
    