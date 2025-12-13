from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AllJobs(http.Controller):
    @http.route('/all-jobs', type='http', auth='public', website=True, method=['GET'], csrf=False)
    def all_jobs(self):
        try:
            # Fetch jobs from hr.jobs model
            jobs = request.env['hr.job'].sudo().search([])
            if jobs:
                _logger.info('Jobs found: %s', jobs)
                return request.render('job_portal.all_jobs', {'jobs': jobs})
            else:
                _logger.info('No jobs found')
                return request.render('job_portal.all_jobs', {'jobs': []})
        except Exception as e:
            _logger.error('Error fetching jobs: %s', e)
            return request.render('job_portal.all_jobs', {'jobs': []})