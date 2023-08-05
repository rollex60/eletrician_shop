from django.db import models
from django.urls import reverse


class Electric(models.Model):
    # ----Electric block-----------------------------------------------------------------------------

    name = models.CharField(max_length=255, verbose_name="Titulo")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Contente")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Foto")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Tempo criar")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Tempo atualização")
    is_published = models.BooleanField(default=True, verbose_name="Está publicado")
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='rubrics', verbose_name="Category")

    def __str__(self):
        return self.name

    # Link to post
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Article'
        ordering = ['-time_create', 'name']


class Category(models.Model):
    # ----Category-----------------------------------------------------------------------------

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
        ordering = ['id']

    # Link to category
    def get_absolut_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})