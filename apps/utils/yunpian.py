# _*_ coding: utf-8 _*_
__author__ = 'Ctrl'
__date__ = '011 18/05/11 下午  17:03'

import requests
import json

class YunPian(object):
    def __init__(self,api_key ):
        self.api_key = api_key
        self.single_send_url ='发送单条短信的url'

    def send_sms(self,code,mobile):
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            'text':'【慕学生鲜】您的验证码是{code}，如非本人操作，请忽略本短信'.format(code=code),

        }
        response = requests.post(self.single_send_url,data=parmas)
        re_dict = json.loads(response.text)#获取返回值
        return re_dict

#测试
if __name__ == "__main__":
    yun_pian = YunPian("apikey")
    yun_pian.send_sms("2017",'15622241321')