from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import Blog, Category, Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'blog', 'main_content', 'content', 'authors_paragraph', 'authors_signature', 'photo', 'tages', 'is_published', 'get_html_photo', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Miniature"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)