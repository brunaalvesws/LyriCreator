from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import QueryDict


class index(View):
    login_url = '/auth/login/'
    http_method_names = ['post', 'get']

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def get(self, request, *args, **kwargs):
        template = loader.get_template('creation/interface.html')
        context = {'resultado': 1}
        return HttpResponse(template.render(context, request))
    
    def post(self, request, *args, **kwargs):
        artista1 = request.POST.get('artist1')
        artista2 = request.POST.get('artist2')
        mistura = request.POST.get('mistura')

        data = {}
        template_name = 'creation/result.html'
        context = {'resultado':artista2}
        data['result'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)

