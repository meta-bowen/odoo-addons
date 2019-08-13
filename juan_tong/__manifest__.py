# -*- coding: utf-8 -*-

{
    'name': '微信卡券引流平台',
    'version': '0.1',
    'category': 'New Retail',
    'description': """
微卷通后台
========================================
* 提供后台数据维护入口
* 提供前端数据与应用接口
""",
    'depends': ['base_setup','web','website',],
    'data': [
		'security/juantong_security.xml',
		'security/activity_security.xml',
		'security/account_security.xml',
		'security/indent_security.xml',
    	'security/ir.model.access.csv',

    	'views/juantong_menu.xml',
    	'views/juantong_view.xml',
		'views/activity_menu.xml',
		'views/activity_view.xml',
		'views/indent_menu.xml',
		'views/indent_view.xml',
		'views/account_menu.xml',
		'views/account_view.xml',
    	'views/city.xml',
		'data/indent_sequence_data.xml',

		'views/activity_template.xml',
		'views/card_template.xml',


],
	'qweb': [
        "static/src/xml/ticket_views.xml",
		"static/src/xml/widget_template.xml",
		"static/src/xml/test.xml"
    ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
