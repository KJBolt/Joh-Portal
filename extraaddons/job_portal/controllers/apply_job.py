from odoo import http
from odoo.http import request
import base64
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ApplyJob(http.Controller):

    # Handle job application page
    @http.route('/apply-job/<int:job_id>', type='http', auth='public', website=True, method=['GET'], csrf=False)
    def apply_job(self, job_id):
        job = request.env['hr.job'].sudo().search([('id', '=', job_id)])
        return request.render('job_portal.apply_job', {'job': job})
    

    # Handle job application form submission
    @http.route('/apply-job/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def submit_application(self, **post):
        """Handle job application form submission"""
        
        # Log all form values
        _logger.info("="*50)
        _logger.info("Job Application Submitted")
        _logger.info("="*50)
        _logger.info(f"Full Name: {post.get('fullname')}")
        _logger.info(f"Email Address: {post.get('email_address')}")
        _logger.info(f"Phone Number: {post.get('phone_number')}")
        _logger.info(f"Expected Salary: {post.get('expected_salary')}")
        _logger.info(f"Start Date: {post.get('start_date')}")
        _logger.info(f"Portfolio URL: {post.get('portfolio_url')}")
        _logger.info(f"LinkedIn Profile: {post.get('linkedin_profile')}")
        _logger.info(f"Cover Letter: {post.get('cover_letter')}")
        _logger.info(f"Job ID: {post.get('job_id')}")
        _logger.info(f"Department ID: {post.get('department_id')}")
        
        # Log file uploads if present
        if post.get('image_proposal'):
            _logger.info(f"Image Proposal: {post.get('image_proposal').filename if hasattr(post.get('image_proposal'), 'filename') else 'File uploaded'}")
        if post.get('video_proposal'):
            _logger.info(f"Video Proposal: {post.get('video_proposal').filename if hasattr(post.get('video_proposal'), 'filename') else 'File uploaded'}")
        if post.get('resume'):
            _logger.info(f"Resume: {post.get('resume').filename if hasattr(post.get('resume'), 'filename') else 'File uploaded'}")
        
        _logger.info("="*50)
        
        # Create applicant record in Odoo
        try:
            job_id = int(post.get('job_id'))
            
            # Get job details for the application name
            job = request.env['hr.job'].sudo().browse(job_id)
            application_name = f"Application for {job.name}" if job else "Job Application"
            
            # Create the applicant
            applicant_vals = {
                'name': application_name,  # Required field
                'partner_name': post.get('fullname'),
                'partner_phone': post.get('phone_number'),
                'email_from': post.get('email_address'),
                'linkedin_profile': post.get('linkedin_profile'),
                'job_id': job_id,
                # 'department_id': job_id.department_id.id,
                'description': post.get('cover_letter', 'Not Specified'),
                'salary_expected': post.get('expected_salary', ''),
                'availability': post.get('start_date'),
            }
            
            # Add availability if provided
            if post.get('start_date') and post.get('start_date').strip():
                applicant_vals['availability'] = post.get('start_date')
            
            # Add image proposal if uploaded
            if post.get('image_proposal') and hasattr(post.get('image_proposal'), 'read'):
                image_file = post.get('image_proposal')
                image_data = base64.b64encode(image_file.read())
                applicant_vals['image_proposal'] = image_data
                applicant_vals['image_proposal_filename'] = image_file.filename
                _logger.info(f"Added image proposal: {image_file.filename}")
            
            # Add video proposal if uploaded
            if post.get('video_proposal') and hasattr(post.get('video_proposal'), 'read'):
                video_file = post.get('video_proposal')
                video_data = base64.b64encode(video_file.read())
                applicant_vals['video_proposal'] = video_data
                applicant_vals['video_proposal_filename'] = video_file.filename
                _logger.info(f"Added video proposal: {video_file.filename}")
            
            applicant = request.env['hr.applicant'].sudo().create(applicant_vals)
            _logger.info(f"Created applicant record with ID: {applicant.id}")
            
            # Attach CV/Resume as a file attachment
            if post.get('resume') and hasattr(post.get('resume'), 'read'):
                resume_file = post.get('resume')
                resume_data = base64.b64encode(resume_file.read())
                request.env['ir.attachment'].sudo().create({
                    'name': resume_file.filename,
                    'type': 'binary',
                    'datas': resume_data,
                    'res_model': 'hr.applicant',
                    'res_id': applicant.id,
                    'mimetype': resume_file.content_type,
                })
                _logger.info(f"Attached CV/Resume: {resume_file.filename}")
            
        except Exception as e:
            _logger.error(f"Error creating applicant: {str(e)}")
            raise UserError(f"Error creating applicant, {str(e)}")
            # Don't raise error to avoid transaction rollback, just log it
        
        # Redirect to success page
        return request.redirect('/application-submitted')
