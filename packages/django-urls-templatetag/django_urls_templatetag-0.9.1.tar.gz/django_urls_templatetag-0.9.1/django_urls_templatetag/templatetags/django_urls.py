import json

from django import template

from ..utils import get_url_templates

register = template.Library()


@register.inclusion_tag("django_urls_templatetag/urls_js.html")
def django_urls_script(*apps):
	url_templates = json.dumps(get_url_templates(*apps))
	return {"url_templates_obj": url_templates}
