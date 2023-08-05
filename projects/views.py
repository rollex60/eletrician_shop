from django import views
from django.shortcuts import render

from electric.mixins import CartMixin, NotificationsMixin
from electric.models import Electric
from electric.utils import menu
from projects.models import *


class ProjectsDetailView(CartMixin, NotificationsMixin, views.generic.DetailView):
# ----Projects---------------------------------------------------------------------------------------
    model = Electric
    template_name = 'gallery.html'
    context_object_name = 'projects'

    def get(self, request, *args, **kwargs):
        projects = Projects.objects.all().order_by('-id')
        residences = Residences.objects.all().order_by('-id')
        industrial = Industrial.objects.all().order_by('-id')
        offices = Offices.objects.all().order_by('-id')
        retail = Retail.objects.all().order_by('-id')
        heating = Heating.objects.all().order_by('-id')
        aircond = AirConditioning.objects.all().order_by('-id')
        securitysystems = SecuritySystems.objects.all().order_by('-id')
        electrical = Electrical.objects.all().order_by('-id')
        electricalgallery = ElectricalGallery.objects.all().order_by('-id')
        return render(request, 'gallery.html',
                      {"cart": self.cart,
                       'projects': projects,
                       'residences': residences,
                       'industrial': industrial,
                       'offices': offices,
                       'retail': retail,
                       'heating': heating,
                       'aircond': aircond,
                       'securitysystems': securitysystems,
                       'electrical': electrical,
                       'electricalgallery': electricalgallery,
                       'menu': menu,
                       'notifications': self.notifications(request.user)})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Projects - ' + str(context['gallery'][0].gallery)
        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart
        context['menu'] = menu
        context['gallery_selected'] = context['gallery'][0].gallery_id
        return context
