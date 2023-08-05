from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from utils import upload_function

class Projects(models.Model):
# ----Projects-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='projects', verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Projects'
        verbose_name_plural = 'Projects'
        ordering = ['-time_create', 'name']


class Residences(models.Model):
# ----Residences-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='residences',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Residences'
        verbose_name_plural = 'Residences'
        ordering = ['-time_create', 'name']


class Industrial(models.Model):
# ----Industrial-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='industrial',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Industrial'
        verbose_name_plural = 'Industrial'
        ordering = ['-time_create', 'name']


class Offices(models.Model):
# ----Offices-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='offices',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Offices'
        verbose_name_plural = 'Offices'
        ordering = ['-time_create', 'name']


class Retail(models.Model):
# ----Retail-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='retail',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Retail'
        verbose_name_plural = 'Retail'
        ordering = ['-time_create', 'name']


class ElectricalGallery(models.Model):
# ----Electrical Gallery-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='electricalgallery',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Electrical Gallery'
        verbose_name_plural = 'Electrical Gallery'
        ordering = ['-time_create', 'name']


class Heating(models.Model):
# ----Heating-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='heating',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Heating'
        verbose_name_plural = 'Heating'
        ordering = ['-time_create', 'name']


class AirConditioning(models.Model):
# ----Air Conditioning-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='aircond',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Air Conditioning'
        verbose_name_plural = 'Air Conditioning'
        ordering = ['-time_create', 'name']


class SecuritySystems(models.Model):
# ----Security Systems-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='securitysystems',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Security Systems'
        verbose_name_plural = 'Security Systems'
        ordering = ['-time_create', 'name']


class Electrical(models.Model):
# ----Electrical-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    img_projects = models.ForeignKey('Imgprojects', on_delete=models.CASCADE, related_name='electrical',
                                     verbose_name="imgprojects")
    gallery = GenericRelation('gallery')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return f"{self.id}{self.name}"

    class Meta:
        verbose_name = 'Electrical'
        verbose_name_plural = 'Electrical'
        ordering = ['-time_create', 'name']


class ImgProjects(models.Model):
# ----Img Projects-------------------------------------------------------------------------------------------------
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Imgprojects'
        verbose_name_plural = 'Imgprojects'
        ordering = ['id']

    # Link to category
    def get_absolute_url(self):
        return reverse('projects', kwargs={'projects_slug': self.slug})


class Gallery(models.Model):
# ----Image Gallery----------------------------------------------------------------------------------------
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)
    use_in_slider = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="200px"')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = verbose_name
