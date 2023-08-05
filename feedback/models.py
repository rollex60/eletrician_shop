from django.db import models



class Feedback(models.Model):
    # ----Feedback form---------------------------------------------------------------------------------
    name = models.CharField(max_length=120, verbose_name='Name')
    email = models.EmailField(max_length=120, verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name='Phone', blank=True, null=True)
    call_time = models.CharField(max_length=120, blank=True, null=True, verbose_name='Call time')
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='Date')
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Feedback form'
        verbose_name_plural = 'Feedback form'
