# Generated by Django 4.1.10 on 2023-08-02 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Electric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Titulo')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, verbose_name='Contente')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Foto')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Tempo criar')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Tempo atualização')),
                ('is_published', models.BooleanField(default=True, verbose_name='Está publicado')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rubrics', to='electric.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Article',
                'ordering': ['-time_create', 'name'],
            },
        ),
    ]