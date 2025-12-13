from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome



class CustomAuthSignup(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        """ Override default signup to redirect after successful registration """
        response = super(CustomAuthSignup, self).web_auth_signup(*args, **kw)
        
        # If signup was successful, redirect to your custom URL
        if request.params.get('login') and not isinstance(response, dict):
            user = request.env['res.users'].sudo().search([('login', '=', request.params.get('login'))], limit=1)
            if user:
                # redirect to a specific profile page, you can also make it dynamic
                return request.redirect(f'/profile')
        return response

