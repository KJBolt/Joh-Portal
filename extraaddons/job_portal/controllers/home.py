from odoo import http
from odoo.http import request

class Home(http.Controller):
    @http.route('/', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def index(self):

        domain = []
        domain.append(('website_published', '=', True))

        jobs = request.env['hr.job'].sudo().search(domain, limit=4)

        # Get departments with job counts
        departments = []
        dept_records = request.env['hr.department'].sudo().search([])

        for dept in dept_records:
            job_count = request.env['hr.job'].sudo().search_count([
                ('department_id', '=', dept.id),
                ('website_published', '=', True)
            ])

            if job_count > 0:  # Only show departments with jobs
                departments.append({
                    'name': dept.name,
                    'job_count': job_count,
                    'id': dept.id
                })

        return request.render('job_portal.home', {
            'jobs': jobs,
            'departments': departments
        })
    