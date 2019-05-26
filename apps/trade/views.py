from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from django.contrib.messages.views import SuccessMessageMixin

from utils.permissions import IsOwnerOrReadOnly
from .serializer import ShopCartSerializer,ShopCartDetailSerializer,OrderSerializer,OrderDetailSerializer
from .models import ShoppingCart,OrderInfo,OrderGoods

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车
    list:
        获取购物车列表
    create:
        加入购物车
    delete:
        删除购物车中某一商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ShopCartSerializer  # 设置序列化类为自定义的类
    #queryset = ShoppingCart.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action =='list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


class OrderViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    订单管理
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = OrderSerializer  # 设置序列化类为自定义的类
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action=="retrieve":
            return OrderDetailSerializer
        return OrderSerializer


    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order
