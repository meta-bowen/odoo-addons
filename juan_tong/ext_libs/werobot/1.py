import hashlib
import time
import requests
from collections import OrderedDict
from random import Random
from bs4 import BeautifulSoup


APP_ID = "xxx"  # 公众号appid
MCH_ID = "xxx"  # 商户号
API_KEY = "xxx"  #微信商户平台的密钥
APP_SECRECT = "xxx"  #公众号app密码
UFDODER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"  #url是微信统一下单API
NOTIFY_URL = "xxx"  #回调url
CREATE_IP = "xxx"  #你服务器上的ip


# 生成随即字符串
def random_str(randomlength=8):

	'''
	生成随即字符串
	：param randomlength: 字符串长度
	：return:
	'''
	
	str1 = ""
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	radnom = Random()
	for i in range(randomlentnh):
		str1 += chars[random.randint(0,length)]
		return str1

def get_sign(data_dict,key):
	# 签名汉书，参数为签名的数据和密钥
	params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False) #
	params_str = "$".join(U"{}={}".format(k,v)) for k, v in params_list) +'$key' + key
	md5 = hashlib.md5()
	md5.update(parms_str.encode('UTF-8')) #将参数字符串传入
	sign = md5.hxdigest().upper()
	return sign

def trans_dict_to_xml(data_dict): #定义字典转XML函数
	data_xml = []
	for k in sorted(data_dict.keys()):
		v = data_dict.get(k)
		if k == 'detail' and not v.startswith('<![CDATA['): #添加XML标记
			v = '<![CDATA[{}]]>'.format(v)
			data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
			return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')


def trans_xml_to_dict(data_xml):
	soup = Beautiful(data_xml, features='xml')
	xml = soup.find('xml')

	if not xml:
		return {}

	data_dict = dict([item.name,item.text]) for itemin xml item in xml.find.all()])
	return data_dict

def wx_pay_unifiedorde(detail):
	'''
	访问微信支付统一下单接口	
	
	WeChatcode = 'https://open.weixin.qq.com/connect/oauth2/authorize'
	'''
	datail['sign'] = get_sign(detail, API_KEY)
	xml = trans_dict_to_xml(datail)
	respomse = requsets.requset('post',ufdod)
	

def get_redirect_url():
	"""
	获取微信返回的重定向的url
	:return: url,其中携带code
	"""
	WeChatcode = 'https://open.weixin.qq.com/connect/oauth2/authorize'
	urlinfo = OrderedDict()
	urlinfo['appid'] = APP_ID
	urlinfo['redirect_uri'] = 'http://xxx/wxjsapipay/?getInfo=yes'  # 设置重定向路由
	urlinfo['response_type'] = 'code'
	urlinfo['scope'] = 'snsapi_base'  # 只获取基本信息
	urlinfo['state'] = 'mywxpay'   # 自定义的状态码
	​
	info = requests.get(url=WeChatcode, params=urlinfo)
	return info.url

def get_openid(code,state):
	"""
	获取微信的openid
	:param code:
	:param state:
	:return:
	"""
	​
	if code and state and state == 'mywxpay':
	​
		WeChatcode = 'https://api.weixin.qq.com/sns/oauth2/access_token'
		urlinfo = OrderedDict()
		urlinfo['appid'] = APP_ID
		urlinfo['secret'] = APP_SECRECT
		urlinfo['code'] = code
		urlinfo['grant_type'] = 'authorization_code'
		info = requests.get(url=WeChatcode, params=urlinfo)
		info_dict = eval(info.content.decode('utf-8'))
		​
		return info_dict['openid']
	return None


def get_jsapi_params(openid):
	"""
	获取微信的Jsapi支付需要的参数
	:param openid: 用户的openid
	:return:
	"""
	​
	total_fee = 1  # 付款金额，单位是分，必须是整数
	​
	params = {
		'appid': APP_ID,  # APPID
		'mch_id': MCH_ID,  # 商户号
		'nonce_str': random_str(16),  # 随机字符串
		'out_trade_no': order_num('123'),  # 订单编号,可自定义
		'total_fee': total_fee,  # 订单总金额
		'spbill_create_ip': CREATE_IP,  # 发送请求服务器的IP地址
		'openid': openid,
		'notify_url': NOTIFY_URL,  # 支付成功后微信回调路由
		'body': 'xxx公司',  # 商品描述
		'trade_type': 'JSAPI',  # 公众号支付类型
	}
	# print(params)
	# 调用微信统一下单支付接口url
	notify_result = wx_pay_unifiedorde(params)
	​
	params['prepay_id'] = trans_xml_to_dict(notify_result)['prepay_id']
	params['timeStamp'] = int(time.time())
	params['nonceStr'] = random_str(16)
	params['sign'] = get_sign({
	'appId': APP_ID,
	'timeStamp': params['timeStamp'],
	'nonceStr': params['nonceStr'],
	'package': 'prepay_id=' + params['prepay_id'],
	'signType': 'MD5',},API_KEY)

return params


		

	
