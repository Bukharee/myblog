from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class Portfolio(TemplateView):
    template_name: str = "index.html"

class ProjectsList():
    pass

class Experience():
    pass

class Skills():
    pass

class Education():
    pass
