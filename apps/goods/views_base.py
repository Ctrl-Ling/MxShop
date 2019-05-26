# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '004 18/05/04 下午  19:33'


from django.views.generic.base import View
from goods.models import Goods


class GoodsListView(View):
    def get(self,request):
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     # json_dict = {}
        #     # json_dict["name"] = good.name
        #     # json_dict["category"] = good.category.name
        #     # json_dict["market_price"] = good.market_price
        #     # json_list.append(json_dict)
        #from django.forms.models import model_to_dict
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)




        import json

        from django.core import serializers
        json_data = serializers.serialize("json", goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse,JsonResponse
        return JsonResponse(json_data,safe=False)
        #return HttpResponse(json.dumps(json_data),content_type="application/json")
        #json.dumps是为json_list做序列化