from odoo import models, fields, api

class Profile(models.Model):
    _name = 'job.profile'
    _description = 'Job Profile'
    

    # Basic Information
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    email = fields.Char(string='Email')
    phone_no = fields.Char(string='Phone')
    about_me = fields.Text(string='About Me')
    location = fields.Char(string='Location')
    profile_photo = fields.Binary(string='Profile Photo', attachment=True)



    # Professional Information
    professional_title = fields.Char(string='Professional Title')
    is_verified = fields.Boolean(string='Is Verified')
    experience_level = fields.Char(string='Experience Level')
    availability = fields.Char(string='Availability')
    professional_description = fields.Text(string='Professional Description')
    certification = fields.Char(string='Certification')
    preferred_job_type = fields.Char(string='Preferred Job Type')
    job_category_id = fields.Many2one('hr.job.category', string='Job Category')
    skills_id = fields.Many2one('hr.skill', string='Skills')
    hourly_rate = fields.Float(string='Hourly Rate')
    porfolio_images = fields.Binary('Portfolio Images', attachment=True)
    