import datetime
from calendar import monthrange

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from utils.uploading import upload_function
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import connection, timezone
from django.db import connection


class Blog(models.Model):
    # ----Blog content block----------------------------------------------------------------------------
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Article author', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    main_content = models.TextField(verbose_name="Main content", blank=True, null=True)
    authors_paragraph = models.TextField(verbose_name="Authors paragraph", blank=True, null=True)
    authors_signature = models.CharField(max_length=255, verbose_name="Author's signature", blank=True, null=True)
    content = RichTextUploadingField(blank=True, verbose_name="Contente")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Photo")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    is_published = models.BooleanField(default=True, verbose_name="Is published")
    blog = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='blog', verbose_name="Category")
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)
    tages = TaggableManager(blank=True, related_name='tages')

    def __str__(self):
        return f"{self.id} | {self.name}"

    # Link to post
    def get_absolute_url(self):
        return reverse('blogpost', kwargs={'blogpost_slug': self.slug})

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'
        ordering = ['-id']


class Category(models.Model):
    # ----Category-------------------------------------------------------------------------------------
    
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
        ordering = ['id']

    def get_absoluted_url(self):
        return reverse('blog', kwargs={'blog_slug': self.slug})


class Comment(models.Model):
    # ----Comments--------------------------------------------------------------------------------------
    
    article = models.ForeignKey(Blog, on_delete=models.CASCADE,
                                verbose_name='blogpost', blank=True, null=True, related_name='comments_blog')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Article author', related_name='blog_comments', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Article comments')
    status = models.BooleanField(verbose_name='Article visibility', default=False)

    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'
        ordering = ['-id']
