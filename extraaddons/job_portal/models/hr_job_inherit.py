from odoo import models, fields, api

class JobBenefit(models.Model):
    _name = 'hr.job.benefit'
    _description = 'Job Benefits'
    
    name = fields.Char(string='Benefit Name', required=True)
    color = fields.Integer(string='Color Index')

class JobRequirements(models.Model):
    _name = 'hr.job.requirement'
    _description = 'Job Requirements'
    
    name = fields.Text(string='Specify Requirements', required=True)
    
    def action_delete_requirement(self):
        """Delete requirement from the database"""
        self.unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

class HRJobInherit(models.Model):
    _inherit = 'hr.job'

    salary = fields.Char(string='Salary', required=True, default="Negotiable")
    requirement_ids = fields.Many2many('hr.job.requirement', string='Requirements', required=True)
    company = fields.Char(string='Company', required=True)
    about_company = fields.Text(string="About Company", required=True)
    benefit_ids = fields.Many2many('hr.job.benefit', string='Benefits')