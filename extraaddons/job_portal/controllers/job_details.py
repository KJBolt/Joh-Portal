from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class JobDetails(http.Controller):
    @http.route('/job-details/<int:job_id>', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def job_details(self, job_id, **kwargs):
        try:
            # Fetch the specific job by ID
            job = request.env['hr.job'].sudo().browse(job_id)
            
            if not job:
                _logger.warning('Job with ID %s not found', job_id)
                return request.render('job_portal.job_details', {'job': [],})
            
            _logger.info('Job details fetched: %s', job.name)
            return request.render('job_portal.job_details', {'job': job})
        except Exception as e:
            _logger.error('Error fetching job details: %s', e)
            return request.render('job_portal.job_details', {'job': []})