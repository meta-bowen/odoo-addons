from odoo import http
from odoo.http import request

class Page(http.Controller):
    """
    渲染前端页面路由
    """
    @http.route('/odoo/activity/<page>', auth="public", website=True)
    def activity(self, page, **kwargs):
        """
        activity page
        :param page: activity_name
        :param kwargs:
        :return: activity page
        """
        Num = request.env['activity'].sudo()
        num = Num.search([('name', '=', page)])
        Inden = request.env['indent'].sudo()
        inden = Inden.search([])
        if num:
            return http.request.render('juan_tong.activity_web', {'orders': inden, 'docs': num})
        else:
            return "<h1>活动已结束或不存在<h1>"

    @http.route('/odoo/card', auth="public", website=True)
    def card(self, **kwargs):
        """
        card page
        :param page:
        :param kwargs:
        :return:
        """
        Indent = request.env['indent'].sudo()
        indent = Indent.search([])

        return http.request.render('juan_tong.card_web', {'orders': indent})



