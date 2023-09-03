""" Views """

from django import shortcuts
from django.views.generic import base
from django.http import HttpRequest, HttpResponse
from datetime import datetime
import os
import json

class HomePage(base.TemplateView):
    """Home page view."""

     # Template name
    template_name = "home.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {}
        analysis_str = self._read_result()
        analysis = json.loads(analysis_str.replace("'", '"'))
        context['errors'] = [ datetime.fromtimestamp(record/1000).strftime("%b %d %H:%M:%S:%f") for record in analysis['device_error_records']]
        context['analysis'] = analysis_str

        return shortcuts.render(request, self.template_name, context)
    
    def _read_result(self):
        result_file_path = os.path.join(os.getcwd(), 'parsing_log', 'test_data', 'test.result')
        with open(result_file_path, 'r') as file:
            analysis_str = file.read()
        return analysis_str
