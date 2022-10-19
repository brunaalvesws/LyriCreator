from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import QueryDict
import re
from unidecode import unidecode
import markovify

import requests as req
from urllib.error import HTTPError
from bs4 import BeautifulSoup


class index(View):
    login_url = '/auth/login/'
    http_method_names = ['post', 'get']

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def normaliza_string(self,texto):
        texto = unidecode(texto)
        return texto

    def obtem_pagina_autor(self, autor, MUSIC_SOURCE):
        url_autor = f"{MUSIC_SOURCE}/{autor}"
        resposta = req.get(url_autor)
        if self.checa_resposta(resposta):
            return BeautifulSoup(resposta.text, "html.parser")
        return None

    def obtem_pagina_musica(self,link,MUSIC_SOURCE):
        url_musica = f"{MUSIC_SOURCE}{link}"
        resposta = req.get(url_musica)
        if self.checa_resposta(resposta):
            return BeautifulSoup(resposta.text, "html.parser")
        return None

    def checa_resposta(self,resposta_requests):
        if resposta_requests.status_code != 200:
            return False
        return True

    def obtem_titulo_musica(self,pagina_musica):
        try:
            titulo_musica = pagina_musica.find("div",{"class":"cnt-head_title"})
            titulo_musica = titulo_musica.find("h1").get_text()
        except AttributeError as e:
            titulo_musica = "NA"
        return titulo_musica

    def obtem_letra_musica(self,pagina_musica):
        tags_musica = pagina_musica.find("div", {"class": "cnt-letra"})
        if tags_musica:
            return tags_musica.get_text(strip=True, separator='\n')
        return None

    def get(self, request, *args, **kwargs):
        template = loader.get_template('creation/interface.html')
        context = {'resultado': 1}
        return HttpResponse(template.render(context, request))
    
    def post(self, request, *args, **kwargs):
        artista1 = request.POST.get('artist1')
        artista2 = request.POST.get('artist2')
        mistura = request.POST.get('mistura')

        MUSIC_SOURCE = "https://www.letras.mus.br"
        AUTORES = [artista1, artista2]

        # Abre o arquivo dataset.txt para escrita:
        with open("dataset.txt", "w") as file:

            temporario = ""
            for autor in AUTORES:
                    print(f"\nMinerando musicas de: {autor}")

                    pagina_autor = self.obtem_pagina_autor(autor,MUSIC_SOURCE)
                    lista_musicas = pagina_autor.find("ol", {"class":"cnt-list"}).findAll("li")

                    for musica in lista_musicas:
                        try:
                            a_musica = musica.find("a")

                            if "href" in a_musica.attrs:
                                link = a_musica.attrs['href'] # obtem o link para musica
                                
                                print(f"{MUSIC_SOURCE}{link}")
                                pagina_musica = self.obtem_pagina_musica(link, MUSIC_SOURCE)
                                titulo_musica = self.obtem_titulo_musica(pagina_musica)
                                letra_musica = self.obtem_letra_musica(pagina_musica)
                                if letra_musica != None:
                                    temporario += self.normaliza_string(letra_musica)+"\n"
                                print(f"Musica: {titulo_musica} copiada.")

                                file.writelines(temporario)
                        except:
                            pass

        with open("dataset.txt") as f:
            text = f.read()

        open('dataset.txt', 'w').close()
        # Cria o modelo
        text_model = markovify.NewlineText(text)
 
        final_result = ''
        for i in range(20):
            verso = text_model.make_sentence(tries=30)
            if verso != None:
                final_result += verso
                final_result += "\n"

        data = {}
        template_name = 'creation/result.html'
        context = {'resultado': final_result.split('\n')}
        data['result'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)


