from odoo import http
from odoo.http import request

class JobDetailsNew(http.Controller):
    @http.route('/job-details-new/<int:job_id>', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def job_details_new(self, job_id, **kwargs):
        # Fetch the job
        job = request.env['hr.job'].sudo().browse(job_id)
        
        if not job.exists():
            return request.render('job_portal.job_details_new', {'job': False})
        
        return request.render('job_portal.job_details_new', {
            'job': job,
        })

    @http.route('/share-job/<int:job_id>', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def share_job(self, job_id, **kwargs):
        job = request.env['hr.job'].sudo().browse(job_id)
        if not job.exists():
            return request.not_found()
        
        # Generate share link
        base_url = request.httprequest.url_root
        share_url = f"{base_url}/job-details/{job_id}"
        
        return request.render('job_portal.job_share', {
            'job': job,
            'share_url': share_url,
        })