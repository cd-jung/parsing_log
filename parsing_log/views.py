""" Views """

from django import shortcuts
from django.views.generic import base
from django.http import HttpRequest, HttpResponse
import json

class HomePage(base.TemplateView):
    """Home page view."""

     # Template name
    template_name = "home.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {}
        context['sum'] = 5000
        context['analysis'] = json.dumps({'test':'test'})

        return shortcuts.render(request, self.template_name, context)
