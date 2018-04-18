from django.shortcuts import render
#from django.template import Template, Context
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.models import User
#from Minerva.backend.backend import CustomLDAPAuthBackend
from django.contrib.auth.backends import RemoteUserBackend
from se.search import get_search_results
#from django.template.context import RequestContext
#from django.shortcuts import render_to_response

# Create your views here.
import os
import logging
from aclse.settings import WEBAPP_ROOT

SE_BASE_FE = os.path.join(WEBAPP_ROOT, 'frontend/se')

class SearchMainView(View):
    def get(self, request):
        if(request.GET.get('search_button')=='Click'):
            http_response = self.load_results(request)
            return http_response
        else:
            search_main_view_html = os.path.join(SE_BASE_FE, 'search_main_view.html')
            return render(request, search_main_view_html)

    def load_results(self, request):
        query = request.GET.get('query_in')
        context = get_search_results(query)
        search_results_html = os.path.join(SE_BASE_FE, 'search_results.html')
        return render(request, search_results_html, context)

class SearchResultsView(View):
    def get(self, request):
        search_results_html = os.path.join(SE_BASE_FE, 'search_results.html')
        return render(request, search_results_html)
