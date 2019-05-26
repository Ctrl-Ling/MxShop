# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '004 18/05/04 下午  23:39'

from rest_framework import serializers
from .models import Goods,GoodsCategory,HotSearchWords,GoodsImage


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)



class GoodsSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=True,max_length=100)
    # click_num = serializers.IntegerField(default=0)
    #
    # def create(self, validated_data):
    #     """
    #     可以通过前端传回来的json商品数据创建Goods对象,同时会验证数据的合法性
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return Goods.objects.create(**validated_data)

    #使用ModelSerializer
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ('name','click_num')
        fields = '__all__'#全部字段


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品3级类别序列化
    """

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品2级类别序列化
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    商品1级类别序列化
    嵌套低1级的catgory
    """
    sub_cat = CategorySerializer2(many=True)#sub_cat是2级catgory表，many表示有多个
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"