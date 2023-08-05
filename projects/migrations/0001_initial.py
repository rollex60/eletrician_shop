# Generated by Django 4.1.10 on 2023-08-02 16:53

from django.db import migrations, models
import django.db.models.deletion
import utils.uploading


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgProjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Imgprojects',
                'verbose_name_plural': 'Imgprojects',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SecuritySystems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='securitysystems', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Security Systems',
                'verbose_name_plural': 'Security Systems',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Retail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retail', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Retail',
                'verbose_name_plural': 'Retail',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Residences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residences', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Residences',
                'verbose_name_plural': 'Residences',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Projects',
                'verbose_name_plural': 'Projects',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Offices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offices', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Offices',
                'verbose_name_plural': 'Offices',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Industrial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industrial', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Industrial',
                'verbose_name_plural': 'Industrial',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Heating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heating', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Heating',
                'verbose_name_plural': 'Heating',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=utils.uploading.upload_function)),
                ('use_in_slider', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='ElectricalGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='electricalgallery', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Electrical Gallery',
                'verbose_name_plural': 'Electrical Gallery',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Electrical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='electrical', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Electrical',
                'verbose_name_plural': 'Electrical',
                'ordering': ['-time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='AirConditioning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.uploading.upload_function)),
                ('img_projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircond', to='projects.imgprojects', verbose_name='imgprojects')),
            ],
            options={
                'verbose_name': 'Air Conditioning',
                'verbose_name_plural': 'Air Conditioning',
                'ordering': ['-time_create', 'name'],
            },
        ),
    ]
