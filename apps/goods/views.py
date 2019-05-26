from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from .models import Goods,GoodsCategory,HotSearchWords
from .filters import GoodsFilter
from .serializers import GoodsSerializer,CategorySerializer,HotWordsSerializer
# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):#viewsets与router配套使用
    #商品列表页，分页，过滤，搜索，排序
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')


class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:商品分页列表数据

    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

class HotWordsViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = HotSearchWords.objects.all()
    serializer_class = HotWordsSerializer