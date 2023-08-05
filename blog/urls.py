from django.urls import path, re_path

from .views import *
from . import views


urlpatterns = [
    path('tages/<slug:tag_slug>/', TagBlogView.as_view(), name='tagg'),
    path("search-blog/", SearchResultsBlogView.as_view(), name="search_resultsblog"),
    path('blog/', BlogDetailView.as_view(), name='blog'),
    path('blog/<slug:blog_slug>/', BlogCategory.as_view(), name='blog'),
    # path('catblog/<slug:catblog_slug>/', BlogCategory.as_view(), name='catblog'),
    path('blogpost/<slug:blogpost_slug>/', BlogPost.as_view(), name='blogpost'),


#ajax
    path('updated_comments_status/<int:pk>/<slug:type>', views.updated_comments_status, name='updated_comments_status')
]