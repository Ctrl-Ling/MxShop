# _*_ encoding:utf-8 _*_
from  django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models  import Q
from rest_framework import mixins
from rest_framework import viewsets,status
from rest_framework.response import Response
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerializer,UserRegSerializer,UserDetailSerializer
from utils.yunpian import YunPian
from MxShop.settings import APIKEY
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成4位数字验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in seeds:
            random_str.append(choice(seeds))#从seeds中随机选取一个

        return "".join(random_str)[:4]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)#如果调用失败直接抛出400异常，后面不执行

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status=yun_pian.send_sms(code=code,mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"]
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            },status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    create:
    新建用户
    retrieve:
    获取用户信息
    update:
    修改用户信息
    """
    serializer_class = UserRegSerializer#设置序列化类为自定义的类
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication)
    #permission_classes = (permissions.IsAuthenticated,JSONWebTokenAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer


    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    #重载create实现返回用户token实现注册完就登陆
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        #生成payload,再生成token,放进serializer中的token中
        re_dict = serializer.data
        payload=jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user#获取当前用户


    def perform_create(self, serializer):
        return serializer.save()#返回一个user对象