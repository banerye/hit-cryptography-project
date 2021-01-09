from django.db import models


class BaseModel(models.Model):
    '''abstract model class'''
    is_delete = models.BooleanField(default=False, verbose_name='delete tag')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='update time')

    class Meta:
        abstract = True
