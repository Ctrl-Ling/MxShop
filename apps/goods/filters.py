# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '007 18/05/07 下午  20:02'

from django.db.models import Q
import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    #商品过滤类
    pricemin = django_filters.NumberFilter(name='shop_price',lookup_expr='gt')
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lt')
    #name = django_filters.CharFilter(name='name', lookup_expr='icontains')#忽略大小写在contains前加i。contains是模糊匹配
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        queryset =  queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
        return queryset
    class Meta:
        model = Goods
        fields = ['pricemin','pricemax','is_hot']


