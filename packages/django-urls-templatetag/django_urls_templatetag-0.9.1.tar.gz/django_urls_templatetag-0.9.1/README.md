# Description
`django-urls-templatetag` allows you to reverse django URLs within JavaScript exactly as you do from within Python using the standard `reverse` function.

# Installation and usage
From your django virtual environment, run `pip install django-urls-templatetag`, add `django_urls_templatetag` inside your `INSTALLED_APPS`, then, in your `base.html` template (or any template which defines your JavaScript includes in the HTML `<head>` tag), add `{% load django_urls %}` and then include `{% django_urls_script 'url_namespace1' 'url_namespace2' ... %}` somewhere inside the `<head>` tag of your HTML template, *above* any JavaScript library or code which will make use of this. When you include the `django_urls_script` template tag, you will need to specify which namespaces you want reversed. This is not an automatic process because that could introduce security vulnerabilities by exposing all available URL endpoints. With the template tag included, you can now use a `reverse_url` function within JavaScript.

## Example
Say we have a project which has URLs under an "api" namespace and URLs under a "blog" namespace. In django, we would reverse these with `reverse("api:blog_post_list")` or `reverse("blog:index")` for example. To get the same effect in JavaScript, I would include `{% django_urls_script 'api' 'blog' %}` inside my `<head>` tag in my template. Then, to reverse the URLs from inside JavaScripr, I would do `reverse_url("api:blog_post_list")` or `reverse_url("blog:index")`. Both of these would return as a string the URLs of either endpoint.

Reversing URLs with keyword arguments is also possible. Simply provide the keyword arguments as a JavaScript object as a second argument. An example might look like this: `reverse_url("blog:blog_post_detail", {pk: 55})`. Easy and simple.
