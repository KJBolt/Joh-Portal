from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from logging import getLogger

_logger = getLogger(__name__)


class AuthSignupJobPortal(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        """ Override default signup to redirect after successful registration """
        response = super(AuthSignupJobPortal, self).web_auth_signup(*args, **kw)
        
        # If signup was successful, redirect to your custom URL
        if request.params.get('login') and not isinstance(response, dict):
            user = request.env['res.users'].sudo().search([('login', '=', request.params.get('login'))], limit=1)
            if user:
                # redirect to a specific profile page, you can also make it dynamic
                return request.redirect(f'/')
        return response


    def do_signup(self, qcontext):
        params = request.params if request else qcontext.get('params', {})
        values = {
            'user_role': qcontext.get('user_role') or params.get('user_role'),
        }

        _logger.info("Processing signup with values: %s", values)

        result = super(AuthSignupJobPortal, self).do_signup(qcontext)
        login = qcontext.get('login') or params.get('login')
        _logger.info("Login value: %s", login)

        if login:
            user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
            _logger.info("Found user: %s", user)
            if user:
                # Get group references
                group_portal = request.env.ref('base.group_portal')
                group_user = request.env.ref('base.group_user')
                group_jobseeker = request.env.ref('job_portal.group_jobseeker')
                group_employer = request.env.ref('job_portal.group_employer')

                group_commands = []

                # Determine user type and assign appropriate groups
                if values.get('user_role') in ['jobseeker', 'employer']:
                    # Internal User with specific role group
                    group_commands.append((4, group_user.id))  # Add Internal User
                    group_commands.append((3, group_portal.id))  # Remove Portal User

                    # Add specific role group and remove the other
                    if values['user_role'] == 'jobseeker':
                        group_commands.append((4, group_jobseeker.id))
                        group_commands.append((3, group_employer.id))
                    elif values['user_role'] == 'employer':
                        group_commands.append((4, group_employer.id))
                        group_commands.append((3, group_jobseeker.id))
                else:
                    # Portal User
                    group_commands.append((4, group_portal.id))  # Add Portal User
                    group_commands.append((3, group_user.id))    # Remove Internal User
                    # Remove all role groups
                    group_commands.extend([
                        (3, group_jobseeker.id),
                        (3, group_employer.id)
                    ])

                # Update user with all changes
                user.sudo().write({
                    'groups_id': group_commands,
                    'user_role': values['user_role'],
                })

                _logger.info("Updated user with values: %s and groups: %s", values, group_commands)
                user.clear_caches()

        return result