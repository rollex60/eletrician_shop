from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from projects.models import *


class ProjectGalleryInline(GenericTabularInline):

    model = Gallery
    readonly_fields = ('image_url',)


class ImageProjectsInline(GenericTabularInline):

    model = Gallery
    readonly_fields = ('image_url',)


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class ResidencesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class IndustrialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class OfficesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class RetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class HeatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class AirConditioningAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class SecuritySystemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class ElectricalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class ElectricalGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [ProjectGalleryInline]
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}


class ImgProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Residences, ResidencesAdmin)
admin.site.register(Industrial, IndustrialAdmin)
admin.site.register(Offices, OfficesAdmin)
admin.site.register(Retail, RetailAdmin)
admin.site.register(Heating, HeatingAdmin)
admin.site.register(AirConditioning, AirConditioningAdmin)
admin.site.register(SecuritySystems, SecuritySystemsAdmin)
admin.site.register(Electrical, ElectricalAdmin)
admin.site.register(ElectricalGallery, ElectricalGalleryAdmin)
admin.site.register(ImgProjects, ImgProjectsAdmin)
admin.site.register(Gallery)
