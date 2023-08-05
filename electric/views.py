from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from blog.models import Blog
from electric.mixins import CartMixin, NotificationsMixin
from electric.models import Electric
from electric.utils import menu
from django import views

from projects.models import Projects, Residences, Industrial, Offices, Retail


def about(request):
    return render(request, 'about.html', {'menu': menu, 'name': 'About'})
    

def services(request):
    return render(request, 'services.html', {'menu': menu, 'name': 'Services'})


def prices(request):
    return render(request, 'prices.html', {'menu': menu, 'name': 'Prices'})


def contact(request):
    return render(request, 'contact.html', {'menu': menu, 'name': 'Contact'})


class ElectricHomeDetailView(CartMixin, NotificationsMixin, views.generic.DetailView):
# ----Electric block--------------------------------------------------------------------------------------

    def get(self, request, *args, **kwargs):
        blog = Blog.objects.all().order_by('-id')[:2]
        projects = Projects.objects.all().order_by('-id')[:10]
        residences = Residences.objects.all().order_by('-id')[:10]
        industrial = Industrial.objects.all().order_by('-id')[:10]
        offices = Offices.objects.all().order_by('-id')[:10]
        retail = Retail.objects.all().order_by('-id')[:10]
        return render(request, 'index.html',
                      {"cart": self.cart,
                       'blog': blog,
                       'projects': projects,
                       'residences': residences,
                       'industrial': industrial,
                       'offices': offices,
                       'retail': retail,
                       'menu': menu,
                       'title': 'Eletrician',
                       'notifications': self.notifications(request.user)})
                       
    
