import re

from django.urls import URLPattern, URLResolver, get_resolver
from flatdict import FlatDict


def get_url_template(url_pattern: URLPattern | URLResolver) -> str:
	if hasattr(url_pattern.pattern, "_route"):
		pattern = url_pattern.pattern._route
		pattern = re.sub(r"<(?:[\w]+:)?([\w]+)>", r"{\1}", pattern)
		return pattern
	elif hasattr(url_pattern.pattern, "_regex"):
		pattern = url_pattern.pattern._regex
		pattern = re.sub(r"[\^$?]*", "", pattern)
		pattern = re.sub(r"\(P<([\w]+)>[^)]+\)", r"{\1}", pattern)
		pattern = re.sub(r"[\\.]*{format}", "", pattern)
		pattern = re.sub(r"[+*?]\(.*$", "/", pattern)
		return pattern
	else:
		raise TypeError(
			f"{url_pattern.pattern} is neither a RoutePattern or RegexPattern"
		)


def get_url_templates(*apps):
	url_templates = {}
	resolver = get_resolver()
	patterns = resolver.url_patterns

	def collect_url_templates(patterns: list, app_name: str = None) -> dict:
		url_templates = {app_name: {}}
		for pattern in patterns:
			if isinstance(pattern, URLPattern) and getattr(pattern, "name", None):
				if pattern.name not in url_templates[app_name]:
					url_template = get_url_template(pattern)
					url_templates[app_name][pattern.name] = "/" + url_template
			elif isinstance(pattern, URLResolver):
				prefix = get_url_template(pattern)
				nested_patterns = pattern.url_patterns
				nested_app_name = pattern.app_name or app_name
				tmp = collect_url_templates(nested_patterns, nested_app_name)
				for pattern_name in tmp[nested_app_name]:
					tmp[nested_app_name][pattern_name] = f"/{prefix}" + tmp[
						nested_app_name
					][pattern_name].removeprefix("/")
				for name in tmp:
					if name in url_templates:
						url_templates[name].update(tmp[name])
					else:
						url_templates[name] = tmp[name]
		return url_templates

	url_templates = collect_url_templates(patterns)
	root_url_templates = url_templates.pop(None, None)
	# ideally, we should prevent occluded apps from even being collected,
	# but this is an easy way to do this for now
	if apps:
		tmp = url_templates.copy()
		for app in url_templates:
			if app not in apps:
				tmp.pop(app)
		url_templates = tmp
	url_templates = dict(FlatDict(url_templates))
	if root_url_templates and (not apps or "root" in apps):
		url_templates.update(root_url_templates)
	return url_templates
