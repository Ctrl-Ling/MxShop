# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '011 18/05/11 下午  20:48'
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re #正则表达式包
from datetime import datetime,timedelta
from rest_framework.validators import UniqueValidator


from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
     mobile = serializers.CharField(max_length=11,help_text='手机号')

     def validate_mobile(self, mobile):
        """
        验证手机号码

        """
        #手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        #验证手机号码是否合法
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError("手机号码非法")

        #验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True,max_length=4,min_length=4,#这些参数在rest文档serializer fields中有
                                 help_text="验证码",label="验证码",write_only=True,#此参数表示code字段在序列化时不会被序列化
                                 error_messages={
                                     "blank":"请输入验证码",
                                     "max_length":"验证码格式错误",
                                     "m_length": "验证码格式错误",
                                 })

    username = serializers.CharField(required=True,allow_blank=False,label='用户名',help_text='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(),message="用户已经存在")]
                                     )

    password = serializers.CharField(
        style={'input_type':'password'},label='密码',help_text='密码',write_only=True
    )

    #UniqueValidator用于验证是否有重复数据
    def validate_code(self,code):
        verify_record = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        #self.initial_data时从前端中post过来的数据，验证码按添加时间倒叙排序
        if verify_record:
            last_record = verify_record[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            #验证码5分钟过期，获取当前时间的5分钟之前的时间，看是否小于验证码发送时间,大于则过期
            if five_mintes_ago>last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise  serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    #重写create方法
    def create(self, validated_data):
        user = super(UserRegSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user



    #可作用于全部字段的validate,做一些全局处理
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]#把验证后的验证码删除
        return attrs


    class Meta:
        model = User
        fields = ("username","code","mobile","password")