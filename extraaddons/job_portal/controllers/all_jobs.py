from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AllJobs(http.Controller):
    @http.route('/all-jobs', type='http', auth='public', website=True, method=['GET'], csrf=False)
    def all_jobs(self, **kw):
        try:
            # Search params
            search_query = kw.get('search')
            location_query = kw.get('location')
            job_type = kw.get('job_type')
            contract = kw.get('contract')
            parttime = kw.get('parttime')
            sort = kw.get('sort')

            # Experience Params
            beginner = kw.get('beginner')
            intermediate = kw.get('intermediate')
            senior = kw.get('senior')

            # Get filter parameters
            fulltime = kw.get('fulltime')
            contract = kw.get('contract') 
            parttime = kw.get('parttime')
            permanent = kw.get('permanent')
            salary_range = kw.get('salary_range')

            # Get salary parameters
            salary_min = kw.get('salary_min')
            salary_max = kw.get('salary_max')
            salary_range_option = kw.get('salary_range_option')

            domain = []
            

            # Job type filtering
            job_type_conditions = []
            if fulltime == 'on' or fulltime == 'fulltime':
                job_type_conditions.append(('contract_type_id.name', '=', 'Full-Time'))
            if contract == 'on' or contract == 'contract':
                job_type_conditions.append(('contract_type_id.name', '=', 'Contract'))
            if parttime == 'on' or parttime == 'parttime':
                job_type_conditions.append(('contract_type_id.name', '=', 'Part-Time'))
            if permanent == 'on' or permanent == 'permanent':
                job_type_conditions.append(('contract_type_id.name', '=', 'Permanent'))
            if job_type_conditions:
                domain += ['|'] * (len(job_type_conditions) - 1) + job_type_conditions


            # Salary filtering (assuming salary is stored as numeric string)
            if salary_range_option:
                # Handle predefined ranges
                if salary_range_option == "0-60000":
                    domain.append(('salary', '<=', '60000'))
                elif salary_range_option == "60000-140000":
                    domain += [('salary', '>=', '60000'), ('salary', '<=', '140000')]
                elif salary_range_option == "140000-340000":
                    domain += [('salary', '>=', '140000'), ('salary', '<=', '340000')]
                elif salary_range_option == "340000-850000":
                    domain += [('salary', '>=', '340000'), ('salary', '<=', '850000')]
                elif salary_range_option == "850000-":
                    domain.append(('salary', '>=', '850000'))
            else:
                # Handle custom min/max inputs
                if salary_min:
                    try:
                        min_val = int(salary_min)
                        domain.append(('salary', '>=', min_val))  # No str() conversion needed
                        _logger.info(f"Added salary min filter: {min_val}")
                    except ValueError:
                        pass
                if salary_max:
                    try:
                        max_val = int(salary_max)
                        domain.append(('salary', '<=', max_val))  # No str() conversion needed
                        _logger.info(f"Added salary max filter: {max_val}")
                    except ValueError:
                        pass


            # Experience level filtering
            experience_conditions = []
            if beginner == 'on' or beginner == 'beginner':
                experience_conditions.append(('experience_level', '=', 'beginner'))
            if intermediate == 'on' or intermediate == 'intermediate':
                experience_conditions.append(('experience_level', '=', 'intermediate'))
            if senior == 'on' or senior == 'senior':
                experience_conditions.append(('experience_level', '=', 'senior'))
            if experience_conditions:
                domain += ['|'] * (len(experience_conditions) - 1) + experience_conditions


            # Only show published jobs
            domain.append(('website_published', '=', True))
            
            # If search query
            if search_query:
                domain += ['|',
                    ('name', 'ilike', search_query),
                    ('company', 'ilike', search_query)
                ]
                
            # If location query append to domain
            if location_query:
                domain.append(('address_id.name', 'ilike', location_query))
                
            # Determine the order based on the sort value
            order = 'id desc'  # Default: newest first
            if sort == 'highest_salary':
                order = 'salary asc'
            elif sort == 'newest':
                order = 'id desc'  # You can customize this for relevance
                
            # Filter logic   
            # if job_type or contract or parttime:
            #     domain += [
            #         ('contract_type_id.name', 'ilike', job_type),
            #         ('')
            #         ]
                
            
            jobs = request.env['hr.job'].sudo().search(domain, order=order)
            
            if jobs:
                _logger.info('Jobs found: %s', jobs)
            else:
                _logger.info('No jobs found for search: %s', search_query)
            
            return request.render('job_portal.all_jobs', {
                'jobs': jobs,
                'search_query': search_query,
                'sort': sort
            })
        except Exception as e:
            _logger.error('Error fetching jobs: %s', e)
            return request.render('job_portal.all_jobs', {'jobs': []})