from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
class DemoServey(http.Controller):

    @http.route('/portal/login', type='http', auth='public', website=True,csrf=True)
    def custom_login(self, **kw):
        error = kw.get('error')
        return request.render('demo_servey.login_portal', {
            'error': {
                'csrf': 'Invalid CSRF token. Please try again.',
                'credentials': 'Username and password are required.',
                'login': 'Invalid username or password.'
            }.get(error)
        })
    
    @http.route('/portal/authenticate', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def login_authenticate(self, **post):

        login = post.get('email')
        password = post.get('password')
        
        if http.request.csrf_token():
            http.request.csrf_token()

        try:
            request.session.authenticate(request.env, {
                'type': 'password',
                'login': login,
                'password': password
            })

            return request.redirect('/portal/survey')
        
        except Exception as e:
            return http.request.render('demo_servey.login_portal', {
                'error': _("An unexpected error occurred: %s" % str(e))
            })
    
    @http.route([
        '/portal/survey', 
    ], type='http', auth="user", website=True)
    def portal_all_surveys(self):
        survey_records = request.env['survey.survey'].sudo().search([('associated_users', 'in', request.env.user.id)])
        values = {
            'surveys': survey_records,
            'page_name': 'surveys',     
        }
        return request.render("demo_servey.home_portal", values)  

    @http.route('/portal/survey/start/<int:survey_id>', type='http', auth="user", website=True)
    def start_survey(self, survey_id, **kw):
        survey = request.env['survey.survey'].sudo().browse(survey_id)
        leads_ids = request.env['crm.lead.demo'].sudo().search([('assign_end_users', '=', request.env.user.id)])

        values = {
            'survey': survey,
            'questions': survey.question_ids,  
            'page_name': 'survey_start',
            'available_leads': leads_ids,
        }
        return request.render("demo_servey.portal_survey_start", values)

    @http.route('/portal/survey/submit/<int:survey_id>', type='http', auth="user", website=True, methods=['POST'])
    def submit_survey(self, survey_id, **post):
        survey = request.env['survey.survey'].sudo().browse(survey_id)
        lead_id = post.get('lead_ids')

        responses = request.env['survey.response'].sudo().search_count([
            ('survey_id', '=', int(survey.id)), 
            ('lead', '=', int(lead_id)),
            ('state', '=', 'done')
        ])

        if responses > 0:
            return request.redirect('/portal/survey?error=already_submitted')

        if not survey.exists():
            return request.redirect('/portal/survey')

        answer_lines = []

        for question in survey.question_ids:
            field_name = f"answer_{question.id}"
            answer_value = post.get(field_name, '').strip()

            answer_lines.append((0, 0, {
                'question_id': question.id,         
                'answer': answer_value,
            }))
        p_state = 'done' if post.get('state') == 'd' else 'pending' 

        request.env['survey.response'].sudo().create({
            'name': survey.name + ' - ' + request.env.user.name,
            'survey_id': survey.id,                     
            'answer_ids': answer_lines,          
            "lead": lead_id,
            'user_id': request.env.user.id,
            'state': p_state,
            'sub_state': post.get('state'),
            'comments': post.get('user_comments'),
        })

        return request.redirect('/portal/survey')

    @http.route('/portal/my/surveys', type='http', auth="user", website=True)
    def my_surveys(self, **port):
        survey_records = request.env['survey.response'].sudo().search([('user_id', '=', request.env.user.id)])
        values = {
            'surveys': survey_records,
            'page_name': 'my_surveys',     
        }
        return request.render("demo_servey.my_surveys", values) 

    @http.route('/portal/survey/edit/<int:survey_response_id>', type='http', auth="user", website=True) 
    def edit_survey(self, survey_response_id, **kw):
        survey_response = request.env['survey.response'].sudo().browse(survey_response_id)
        values = {
            'survey': survey_response,
            'questions': survey_response.answer_ids,  
            'page_name': 'edit_survey',
        }
        return request.render("demo_servey.portal_survey_edit", values) 

    @http.route('/portal/survey/save/<int:survey_response_id>', type='http', auth="user", website=True, methods=['POST']) 
    def save_survey(self, survey_response_id, **kw):
        survey_response = request.env['survey.response'].sudo().browse(survey_response_id)
        for question in survey_response.answer_ids:     
            field_name = f"answer_{question.id}"
            answer_value = kw.get(field_name, '').strip()
            question.sudo().write({
                'answer': answer_value,
            })
        return request.redirect('/portal/my/surveys')
        