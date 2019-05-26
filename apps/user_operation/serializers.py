# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '015 18/05/15 下午  21:51'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField( #获取当前登陆的用户
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields = ('user','goods'),
                message="已经收藏",
            )
        ]

        fields = ("user","goods","id")
