from odoo import api, fields, models
import qrcode
from odoo.http import request

#活动
class Activity(models.Model):
	"""
	活动包含某商家活动所含有的卡券
	活动model应与相应的卡券建立绑定
	"""
	_name = 'activity'
	_description = 'Activity'
	name_id = fields.Many2one('shangjia', '门店名称', ondelete='cascade')
	active = fields.Boolean('Active?', default=True)
	name = fields.Char("活动名称", required=True)
	unit_price = fields.Float("单价", required=True)
	original_price = fields.Float("原价", required=True)
	discount = fields.Float('折扣', compute='_compute_discount')
	totalcopies = fields.Integer('总份数')
	residue_copies = fields.Integer('剩余份数', compute='_compute_residue_copies')
	already_sales = fields.Integer('已销量')
	card_receiveds = fields.Integer('领取卡卷量', compute='_compute_card_receiveds')
	start_time = fields.Date('开始时间', required=True)
	end_time = fields.Date('结束时间', required=True)
	OR_code = fields.Char('二维码', default='查看')
	status = fields.Selection([('1', '停用'), ('-1', '启用')], '状态', default='1')

	_sql_constraints = [('name_code_uniq', 'unique(name_id, name)', 'The code of the state must be unique by country state!')]
	date_now = fields.Date('当前时间', default=lambda self: fields.Date.today())

	def _compute_discount(self):
		for price in self:
			price.discount = price.unit_price / price.original_price	

	def _compute_residue_copies(self):
		for card in self:
			card.residue_copies = card.totalcopies - card.already_sales

	@api.depends('already_sales')
	def _compute_card_receiveds(self):
		for card in self:
			card.card_receiveds	= card.already_sales

	@api.multi
	def button_change_status(self):
		
		if self.name_id.status == '-1':
			self.status = str(int(self.status)*(-1))
		
	@api.multi
	def button_QR_code(self):
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=6,
			border=4,
		)

		# 点击进入后直接进行授权跳转
		now_url = request.httprequest.url_root
		qr.add_data('{}odoo/login/{}'.format(now_url, self.name))

		qr.make(fit=True)
		img = qr.make_image()
		img.save('{}.png'.format(self.name))
		img.show()
