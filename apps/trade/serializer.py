# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '018 18/05/18 上午  00:26'

from rest_framework import serializers
import time
from random import Random


from goods.models import Goods
from .models import ShoppingCart,OrderInfo,OrderGoods
from goods.serializers import GoodsSerializer

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = '__all__'#全部字段


class  ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField( #获取当前登陆的用户,并且不会显示到前端
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True,min_value=1,
                                    error_messages={"min_value":"商品数量不小于1",
                                                    "required":"请选择购买数量"
                                                    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(),required=True)

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]#这里是goods对象
        existed = ShoppingCart.objects.filter(user=user,goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed=ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(  # 获取当前登陆的用户,并且不会显示到前端
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)#订单状态不可修改
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)#订单状态不可修改


    def generate_order_sn(self):
        #当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),userid=self.context["request"].user.id,ranstr=random_ins.randint(10,99))
        return order_sn
    def validate(self, attrs):
        attrs["order_sn"]= self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单详情中的商品信息"""
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    """
    获取某一个订单详情（要显示商品信息）
    """
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"