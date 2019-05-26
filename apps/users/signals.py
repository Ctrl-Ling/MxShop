# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '013 18/05/13 下午  22:18'

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:#如果是新建数据库数据的话
        password = instance.password
        instance.set_password(password)
        instance.save()