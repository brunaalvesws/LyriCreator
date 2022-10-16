from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View


class index(View):
    login_url = '/auth/login/'
    http_method_names = ['post', 'get']

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def get(self, request, *args, **kwargs):
        template = loader.get_template('creation/interface.html')
        context = {'resultado': 1}
        return HttpResponse(template.render(context, request))

