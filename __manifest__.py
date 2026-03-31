{
    'name': "demo_servey",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'web', 'website', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/question_servey.xml',
        'views/servey_servey.xml',
        'views/servey_question_answer.xml',
        'views/servey_response.xml',
        'views/crm_leads.xml',
        'views/menu_items.xml',
        'views/login_page.xml',
        'views/home.xml',
        'views/form_page.xml',
        'views/my_survey.xml',
        'views/edit_survery.xml',
        'demo/demo.xml',
    ],

    'assets': {
        'web.login_style': [
            'demo_servey/static/src/css/login.css',
        ],
        'web.home_style': [
            'demo_servey/static/src/css/home.css',
        ],
        'web.servey_style': [
            'demo_servey/static/src/css/servey.css',
        ],
        # 'web.portal_home_style' : [
        #     'ebx_student_portal/static/src/css/home.css',
        # ],
        # 'web.portal_service_style' : [
        #     'ebx_student_portal/static/src/css/service.css',
        # ],
        # 'web.login_app' : [
        #     'ebx_student_portal/static/src/js/login.js',
        # ],
        # 'web.register_Course': [
        #     'ebx_student_portal/static/src/js/regestration.js',
        # ],
        # 'web.register_style': [
        #     'ebx_student_portal/static/src/css/register.css',
        # ],
    },
    # only loaded in demonstration mode

}

