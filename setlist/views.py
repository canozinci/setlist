from django.shortcuts import render

from django.views.generic.base import TemplateView


class OnePageAppView(TemplateView):
    template_name = "index.html"

class OnePageAppView2(TemplateView):
    template_name = "one_page_app2.html"

class TestIndexView(TemplateView):
    template_name = "test_index.html"
