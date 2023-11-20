from django import template
from authentication.forms import LoginForm

register = template.Library()

@register.inclusion_tag('authentication/login_form_modal.html', takes_context=True)
def login_form_modal(context):
    return {'login_form': LoginForm()}
