"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsListViewSet,CategoryViewSet,HotWordsViewSet
from users.views import SmsCodeViewset,UserViewset
from user_operation.views import UserFavViewset
from trade.views import ShoppingCartViewSet,OrderViewSet
#这里是手动将get方法和lists方法绑定起来的方法，使用router可解决
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })


# 配置goods的URL
router = DefaultRouter()
#将GoodsListViewSet注册到router，这样下面的url就不用设置了
#router的主要作用：将create与post方法绑定起来等等
router.register(r'goods', GoodsListViewSet,base_name="goods")
router.register(r'categorys', CategoryViewSet,base_name="categorys")
router.register(r'codes', SmsCodeViewset,base_name="codes")
router.register(r'users', UserViewset,base_name="users")
router.register(r'hotsearchs',HotWordsViewSet,base_name='hotsearchs')
router.register(r'userfavs',UserFavViewset,base_name='userfavs')
router.register(r'shopcarts',ShoppingCartViewSet,base_name='shopcarts')
router.register(r'orders',OrderViewSet,base_name='orders')



urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    #路由配置
    url(r'^', include(router.urls)),

    # path('goods/',goods_list,name="goods-lists"),
    path('docs/',include_docs_urls(title='慕学生鲜')),
    url(r'^api-auth/', include('rest_framework.urls')),
    #drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),#token的url
    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

]
