from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.


class UserFavViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
    返回用户收藏列表

    create:
    用户添加收藏

    retrieve:
    返回某条收藏

    delete:
    删除收藏
    """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)#权限限制,是否登陆,删除的收藏是否本用户的收藏
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)#设置验证
    lookup_field = "goods_id"#设置get方法搜索的对象为goods.id,原本默认搜索对象为id
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)