from django import template
from authentication.forms import LoginForm, SignUpForm

register = template.Library()

@register.inclusion_tag('authentication/login_form_modal.html', takes_context=True)
def login_form_modal(context):
    return {'login_form': LoginForm()}

@register.inclusion_tag('authentication/signup_form_modal.html', takes_context=True)
def signup_form_modal(context):
    return {'signup_form': SignUpForm()}
