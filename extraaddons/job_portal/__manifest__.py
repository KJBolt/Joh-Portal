{
    'name': 'Job Portal',
    'category': 'Generic Modules/Human Resources',
    'author': 'GeoiWorks',
    'version': '17.0.1.0.2',
    'sequence': 3,
    'license': 'LGPL-3',
    'summary': 'Job Portal',
    'description': """Job Portal.""",
    'depends': ['website_hr_recruitment'],
    'data': [
        'views/hide_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [],

        'web.assets_backend': [],
    },
    'images': [],
    'application': True,
}
