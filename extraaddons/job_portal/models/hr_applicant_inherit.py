from odoo import models, fields, api

class HRApplicantInherit(models.Model):
    _inherit = 'hr.applicant'
    
    image_proposal = fields.Binary(string='Image Proposal', attachment=True)
    image_proposal_filename = fields.Char(string='Image Filename')
    video_proposal = fields.Binary(string='Video Proposal', attachment=True)
    video_proposal_filename = fields.Char(string='Video Filename')