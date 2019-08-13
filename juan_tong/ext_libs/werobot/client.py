# -*- coding: utf-8 -*-
import re
import time
import requests
import hashlib
from collections import OrderedDict
import random
from bs4 import BeautifulSoup

from requests.compat import json as _json


# from werobot.utils import to_text


class ClientException(Exception):
    pass


#def check_error(json):
    """
    检测微信公众平台返回值中是否包含错误的返回码。
    如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
    """
    #if "errcode" in json and json["errcode"] != 0:
        #raise ClientException("{}: {}".format(json["errcode"], json["errmsg"]))
    #return json


class Client(object):
    """
    微信 API 操作类
    通过这个类可以方便的通过微信 API 进行一系列操作，比如主动发送消息、创建自定义菜单等
    """

    def __init__(self, appid, appsecret, mchid=0, gooddesc=0, notify_url=0):
        self.appid = appid
        self.appsecret = appsecret
        self.mchid = mchid
        self.key = "wieuro9874297352ssaoqiwUIUEUYwie"
        self.gooddesc = gooddesc
        self.notify_url = notify_url
        self._token = None
        self.token_expires_at = None

    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": self.token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
       	json = r.json()
        #if check_error(json):
        return json

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )

    def grant_token(self):
        """
        获取 Access Token 。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )

    @property
    def token(self):#判断token是否超时
        if self._token:
            now = time.time()
            if self.token_expires_at - now > 60:
                return self._token
        json = self.grant_token()
        self._token = json["access_token"]
        self.token_expires_at = int(time.time()) + json["expires_in"]
        return self._token
    #创建货架接口
    def create_goods(self,data):
        return self.post(
            url="https://api.weixin.qq.com/card/landingpage/create",
            data=data
    )	
    
    #创建卡劵
    def create_card(self, card_data):
        return self.post(
            url="https://api.weixin.qq.com/card/create",
            data=card_data
        )
   
    #获取code
    def get_code(self):
        pass
            

    #获取微信返回的重定向的url
    def get_redirect_url(self):
        WeChatcode = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        urlinfo = OrderedDict()
        urlinfo['appid'] = self.appid
        urlinfo['redirect_url'] = "https://www.datafantasy.cn/mp/notify.html"
        urlinfo['response_type'] = 'code'
        urlinfo['scope'] = "snsapi_userinfo" #授权类型
        urlinfo['state'] = ''  # 自定义的状态码
        patter = re.compile("^response_type=(.+?)\$$")
        info = requests.get(url=WeChatcode, params=urlinfo)
        #print("111111111111111111111111++++",patter.findall(info.url))
        #print("111111111111111111111111++++",type(info.url))
        return info.url

    #获取openid
    def get_openid(self,code):
        return self.get(
            url="https://api.weixin.qq.com/sns/oauth2/access_token",
            params=code
        )

    # 生成随即字符串
    def random_str(self,randomlength=8):
        str1 = ""
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        #radnom = Random()
        for i in range(randomlength):
            str1 += chars[random.randint(0,length)]
        return str1


    #获取用户基本信息
    def get_userinfo(self,openid):
        return self.get(
            url="https://api.weixin.qq.com/sns/userinfo",
            params=openid
        )

    #生成扫码付款订单
    def order_num(self):
        local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        result = 'T' + local_time +random_str(5)
        return result


    #获取sign
    def getSign(self,data):
        # 计算签名
        params_list = sorted(data.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
        params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + self.key
        #print(params_str)
        sign = self.get_MD5(params_str).upper()

        return sign
        

    #MD5函数
    def get_MD5(self,str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()

    #参数转XML
    def get_xml(self,data):
        data['sign'] = self.getSign(data)
        xml = ''
        for key,value in data.items():
            xml += '<{0}>{1}</{0}>'.format(key,value)
        xml = '<xml>{0}</xml>'.format(xml)
        #print(xml)
        return xml

    '''#字典转换为XML
    def trans_dict_to_xml(data_dict): #定义字典转XML的函数
        data_xml = []
        for k in sorted(data_dict.keys()):  #遍历字典排序后的key
        v = data_dict.get(k)  # 取字典中key对应的value
        if k == 'datail' and not v.startswith('<![CDATA[')
    '''
    #XML转字典
    def trans_xml_to_dict(self,data_xml):
        soup = BeautifulSoup(data_xml, features='xml')
        xml = soup.find('xml') # 解析XML
        if not xml:
            return {}
        data_dict = dict([(item.name, item.text) for item in xml.find_all()])
        return data_dict
    #统一下单代码
    def get_order(self, data):
        data['nonce_str'] = self.random_str(8)
        data['spbill_create_ip'] = "127.0.0.1"
        xml = self.get_xml(data)
        #print("22222222222222222222222",xml)    
        resp = requests.post("https://api.mch.weixin.qq.com/pay/unifiedorder", data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
        #print("3333333333333333333",resp.text)
        msg = resp.text.encode('ISO-8859-1').decode('utf-8')
        xmlresp = self.trans_xml_to_dict(msg)
        #print("4444444444444",xmlresp)
        prepay_id = ''

        if xmlresp['return_code'] == 'SUCCESS':
            if xmlresp['result_code'] == 'SUCCESS':
                prepay_id = xmlresp['prepay_id']
                timestamp = str(int(time.time()))
                data = {
                    "appId": xmlresp['appid'],
                    "nonceStr": self.random_str(),
                    "package": "prepay_id=" + xmlresp['prepay_id'],
                    "signType": "MD5",
                    "timeStamp": timestamp
                }
                data['paySign'] = self.getSign(data)
                data['orderid'] = 0
                return data
            else:
                msg = xmlresp['err_code_des']
                return msg
        else:
            msg = xmlresp['return_msg']
            return msg                    

    """获取卡卷信息"""
	
    def get_card(self, card_id):
        return self.post(
            url="https://api.weixin.qq.com/card/get",
            data=card_id
        )
	#获取卡劵列表信息
    def get_cards(self, cards_data):
        return self.post(
            url="https://api.weixin.qq.com/card/batchget",
            data=cards_data
        )
    
    def create_menu(self, menu_data):
        """
        创建自定义菜单 ::

            client = Client("id", "secret")
            client.create_menu({
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]})
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单创建接口

        :param menu_data: Python 字典

        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/create",
            data=menu_data
        )

    def get_menu(self):
        """
        查询自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单查询接口

        :return: 返回的 JSON 数据包
        """
        return self.get("https://api.weixin.qq.com/cgi-bin/menu/get")

    def delete_menu(self):
        """
        删除自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单删除接口

        :return: 返回的 JSON 数据包
        """
        return self.get("https://api.weixin.qq.com/cgi-bin/menu/delete")

    def upload_media(self, media_type, media_file):
        """
        上传多媒体文件。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file:要上传的文件，一个 File-object

        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="http://file.api.weixin.qq.com/cgi-bin/media/upload",
            params={
                "access_token": self.token,
                "type": media_type
            },
            files={
                "media": media_file
            }
        )

    def download_media(self, media_id):
        """
        下载多媒体文件。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件

        :param media_id: 媒体文件 ID

        :return: requests 的 Response 实例
        """
        return requests.get(
            "http://file.api.weixin.qq.com/cgi-bin/media/get",
            params={
                "access_token": self.token,
                "media_id": media_id
            }
        )

    """def create_group(self, name):

        创建分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

        name = to_text(name)
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/create",
            data={"group": {"name": name}}
        )"""

    def get_groups(self):
        """
        查询所有分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :return: 返回的 JSON 数据包
        """
        return self.get("https://api.weixin.qq.com/cgi-bin/groups/get")

    def get_group_by_id(self, openid):
        """
        查询用户所在分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param openid: 用户的OpenID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/getid",
            data={"openid": openid}
        )

    """def update_group(self, group_id, name):
    
        修改分组名
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param group_id: 分组id，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
      
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/update",
            data={"group": {
                "id": int(group_id),
                "name": to_text(name)
            }}
        )"""

    def move_user(self, user_id, group_id):
        """
        移动用户分组
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=分组管理接口

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/members/update",
            data={
                "openid": user_id,
                "to_groupid": group_id
            }
        )

    def get_user_info(self, user_id, lang="zh_CN"):
        """
        获取用户基本信息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取用户基本信息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/user/info",
            params={
                "access_token": self.token,
                "openid": user_id,
                "lang": lang
            }
        )

    def get_followers(self, first_user_id=None):
        """
        获取关注者列表
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取关注者列表

        :param first_user_id: 可选。第一个拉取的OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        params = {
            "access_token": self.token
        }
        if first_user_id:
            params["next_openid"] = first_user_id
        return self.get("https://api.weixin.qq.com/cgi-bin/user/get", params=params)

    def get_media_list(self, media_type, offset, count):
        """
        获取素材列表。
        :param media_type: 素材的类型，图片（image）、视频（video）、语音 （voice）、图文（news）
        :param offset: 从全部素材的该偏移位置开始返回，0表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/material/batchget_material",
            data={
                "type": media_type,
                "offset": offset,
                "count": count
            }
        )

    def send_text_message(self, user_id, content):
        """
        发送文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "text",
                "text": {"content": content}
            }
        )

    def send_image_message(self, user_id, media_id):
        """
        发送图片消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                }
            }
        )

    def send_voice_message(self, user_id, media_id):
        """
        发送语音消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "voice",
                "voice": {
                    "media_id": media_id
                }
            }
        )

    def send_video_message(self, user_id, media_id,
                           title=None, description=None):
        """
        发送视频消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        """
        video_data = {
            "media_id": media_id,
        }
        if title:
            video_data["title"] = title
        if description:
            video_data["description"] = description

        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "video",
                "video": video_data
            }
        )

    def send_music_message(self, user_id, url, hq_url, thumb_media_id,
                           title=None, description=None):
        """
        发送音乐消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :return: 返回的 JSON 数据包
        """
        music_data = {
            "musicurl": url,
            "hqmusicurl": hq_url,
            "thumb_media_id": thumb_media_id
        }
        if title:
            music_data["title"] = title
        if description:
            music_data["description"] = description

        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "music",
                "music": music_data
            }
        )

    def send_article_message(self, user_id, articles):
        """
        发送图文消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param articles: 一个包含至多10个 :class:`Article` 实例的数组
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append({
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "picurl": article.img
            })
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "news",
                "news": {
                    "articles": articles_data
                }
            }
        )

    def send_news_message(self, user_id, media_id, kf_account=None):
        """
        发送永久素材中的图文消息。
        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 媒体文件 ID
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        data = {
            "touser": user_id,
            "msgtype": "mpnews",
            "mpnews": {
                "media_id": media_id
            }
        }
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def create_qrcode(self, **data):
        """
        创建二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/qrcode/create",
            data=data
        )

    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """
        return requests.get(
            url="https://mp.weixin.qq.com/cgi-bin/showqrcode",
            params={
                "ticket": ticket
            }
        )

