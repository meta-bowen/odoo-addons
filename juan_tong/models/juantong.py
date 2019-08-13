from odoo import api, fields, models
from odoo.exceptions import Warning

# 城市        
class City(models.Model):
    _name = 'res.country.city'
    _description = 'City'
    _order = 'display_order'

    state_id = fields.Many2one('res.country.state', string=u'省份', required=True)
    name = fields.Char(string=u'城市', required=True, help='城市名称')
    code = fields.Char(string=u'城市编码', help='城市编码', required=True)
    display_order = fields.Integer(string=u'显示顺序',help=u'从小到大排序',default=0)
    memo = fields.Text(u'备注')  
    
    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, code)', 'The code of the state must be unique by country state !')
    ]

# 行政区划
class District(models.Model):
    _name = 'res.country.district'
    _description = 'District'
    _order = 'display_order'

    city_id = fields.Many2one('res.country.city', string=u'城市', required=True)
    name = fields.Char(string=u'行政区名称', required=True, help='行政区名称')
    display_order = fields.Integer(string=u'显示顺序',help=u'从小到大排序',default=0)
    memo = fields.Text(u'备注')  


class Shangjia(models.Model):
	_name = 'shangjia'
	_description = '商家管理系统'
	
	
	name = fields.Char('门店名称', required=True,)  #required=True，必填项
	id = fields.Integer("编号")
	active = fields.Boolean('Active?', default=True)
	#address_country = fields.Selection([('china','中国'),('other','其他')],'国家')
	#address_city = fields.Selection([('beijing','北京'),('guangdong','广东')],'城市')
	id_district = fields.Many2one("res.country.district", string=u'行政区',domain="[('city_id', '=', id_city)]", ondelete='restrict')
	id_city = fields.Many2one("res.country.city", string=u'城市', domain="[('state_id', '=', id_state_id)]", ondelete='restrict')
	id_state_id = fields.Many2one("res.country.state", string=u'省', domain="[('country_id', '=', id_country_id)]", ondelete='restrict')
	id_country_id = fields.Many2one('res.country', string=u'国家', ondelete='restrict')


	contact = fields.Char("联系人")
	contact_way = fields.Char('联系方式')
	totalcard = fields.Integer("总卡劵")  
	totalcard_left = fields.Integer("剩余总卡劵", compute='_compute_totalcard_left')  #readonly=True，不可编辑
	card_received =  fields.Integer("已领卡劵")

	#status = fields.Selection([('unavailable','停用'),('available','启用')],'状态')
	status = fields.Selection([('1', '停用'), ('-1', '启用')], '状态', default='1')
	
	@api.depends('totalcard', 'card_received')
	def _compute_totalcard_left(self):
		for card in self:
			card.totalcard_left = card.totalcard - card.card_received
			
	@api.multi
	def button_change_status(self):
		self.status = str(int(self.status)*(-1))
		if self.status == '1':
			x = self.env['activity'].search([('name_id', '=', self.name)])
			x.write({'status': '1'})
			return True
			
	#获取token
	@api.multi
	def button_check_test1(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		token = client.grant_token()
		raise Warning('Token: %s' % token)
		return True
	
	#查询卡劵
	@api.multi
	def button_check_test2(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		'''card_data = {
						"card_id":"phCcY1kxEh-eKaKw9UuhSzdJ8BPk"
}'''
		token = client.get_redirect_url()
		raise Warning('Token: %s' % token)
		return True
	#查询卡劵列表
	@api.multi
	def button_check_test3(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		card_data = {
						"offset": 0,
						"count": 10,
						"status_list": ["CARD_STATUS_NOT_VERIFY"]
}
		token = client.get_cards(card_data)
		raise Warning('Token: %s' % token)
		return True

	#创建货架接口
	@api.multi
	def button_check_test4(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		data = {
			"banner":"http://mmbiz.qpic.cn/mmbiz/iaL1LJM1mF9aRKPZJkmG8xXhiaHqkKSVMMWeN3hLut7X7hicFN",
			"page_title": "惠城优惠大派送",
			#"can_share": true,
			"scene": "SCENE_NEAR_BY",
			"card_list": [
				{
					"card_id": "phCcY1lP4G06RXx9IgzcBPiUbNQM",
					"thumb_url": "www.qq.com/a.jpg"
				},
				{
					"card_id": "phCcY1mBa8AQMrCz1SPJsMdf5pxo",
					"thumb_url": "www.qq.com/b.jpg"
				}  
			]
		}
		token = client.create_goods(data)
		#raise Warning('Token: %s' % token)
		return True

	#获取openid接口
	@api.multi
	def button_check_test6(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		code = {
						"appid": "wx7376a2b8c3146546",
						"secret": "877c99113297bb5fd8e41e9e9b831dff",
						"code": "071EHf6k17P2pn06rT5k1hQY5k1EHf62",
						"grant_type": "authorization_code",
				}
		openid = client.get_openid(code)
		raise Warning('Openid: %s' % openid)
		return True

	#获取用户信息接口
	@api.multi
	def button_check_test7(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		card_data = {
						"access_token": "21_r6QEyXCuGR5IrNVro1LcZPHqfK0IwvQwdKkKMnSF8yIV8WBQQLhVn_HJMtux61fs7GDihYVTQUfP0kp0qR9gnA",
						"openid":"orvNk50RFP7zbzvAPziOxwZFKz4s",
						"lang" : "zh_CN "
					}
		userinfo = client.get_userinfo(card_data)
		raise Warning('Userinfo: %s' % userinfo)
		return True

	#微信支付方法
	@api.model
	def get_token(self,appid,secret):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client(appid, secret)
		token = client.grant_token()

		#return self.env.ref('juan_tong.card_web').render({'data':token})
		return token

	#支付接口
	@api.multi
	def button_check_test5(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		data = {
			"appid": "wx7376a2b8c3146546",
			"body": "通讯充值",
			"mch_id":"1534364961",
			"nonce_str": "",			
			"notify_url": "https://www.datafantasy.cn/",
			"openid": "orvNk50RFP7zbzvAPziOxwZFKz4s",
			"out_trade_no": "asd123",
			"spbill_create_ip": "",
			"total_fee": "100",
			"trade_type": "JSAPI",
				}
		order = client.get_order(data)
		appID = order['appId']
		#raise Warning('order: %s' % order)
		return order

	#创建卡劵
	@api.multi
	def button_check_test(self):
		from ..ext_libs.werobot.client import ClientException, Client
		client = Client('wx7376a2b8c3146546', '877c99113297bb5fd8e41e9e9b831dff')
		card_data = {
					"card": {
						"card_type": "GENERAL_COUPON",
						"general_coupon": { 
							"base_info": {
								"logo_url": "http://mmbiz.qpic.cn/mmbiz/lprtsiabGHGz8DfXbIXKhqBuLcuv2SvkguEBBXVwQCI3khyv3IicCxyo0a843ryXwjxicmiaTpGdzyVBUznPzvxKZQ/0",
								"brand_name": "我们789",
								"code_type": "CODE_TYPE_TEXT",
								"title": "苹果",
								"sub_title": "购买只需0.1元",
								"color": "Color010",
								"notice": "购买时请录入优惠码",
								"description": "需要自负邮费，消费金额到达79元可免邮费",
								"date_info": {
									"type": "DATE_TYPE_FIX_TIME_RANGE",
									"begin_timestamp": 1520041600,
									"end_timestamp": 1651577599
								},
								"sku": {
									"quantity": 0
								},
								"get_limit": 1,
								#"use_custom_code": true,
								"get_custom_code_mode":"GET_CUSTOM_CODE_MODE_DEPOSIT",
								#"bind_openid": false,
								#"can_share": false,
								#"can_give_friend": false,
								"center_title": "快速购买",
								"center_sub_title": "立刻把和田枣带回家",
								"center_url": "www.j1.com",
								"custom_url_name": "立即使用",
								"custom_url": "http://www.j1.com",
								"custom_url_sub_title": "去键一网购买",
								"promotion_url_name": "更多活动",
								"promotion_url": "http://www.ijkang.com.",
								"source": "我们爱健康"
							},
							"default_detail": "1分钱购买"
						}
					}
				}
		token = client.create_card(card_data)
		raise Warning('Token: %s' % token)
		return True


			
			
			

	
	
	
	

