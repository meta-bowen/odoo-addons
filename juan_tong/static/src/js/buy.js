odoo.define('juan_tong.button_buy', function(require){
'use strict';
var core = require('web.core');
var session = require('web.Session');
var Widget = require('web.Widget');
var User = require('juantong.share').Ticket;
var rpc = require('web.rpc');
var ajax = require('web.ajax');
var qweb = core.qweb;
var _t = core._t;

require('web.dom_ready');



var BuyButton = Widget.extend({
    template: 'buy.template',
    events: {
        'click .o_buynow': '_onClick',
    },
    xmlDependencies: ['/juan_tong/static/src/xml/widget_template.xml'],

    init: function () {
        this.base_url = 'http://www.ai-solution.cn/';
    },
    _onClick: function () {
        alert('微信支付事件');
        ajax.rpc(this.base_url + "odoo/pay/create",{}).then(function(res){
            var data = JSON.parse(res);
//            this.data_type = typeof(data);
//            this.appId = data.appId;
//            console.log('data >>> ',data);
//            console.log('data_type >>> ',this.data_type);
//            console.log('appId >>> ',this.appId);
            WeixinJSBridge.invoke(
                'getBrandWCPayRequest', {
                 "appId":data.appId, //公众号名称，由商户传入
                 "timeStamp":data.timeStamp, //时间戳，自1970年以来的秒数
                 "nonceStr":data.nonceStr, //随机串
                 "package":data.package,
                 "signType":data.signType, //微信签名方式
                 "paySign":data.sign, //微信签名
                },
                function(res){
                    if(res.err_msg == "get_brand_wcpay_request:ok" ){
                        console.log("支付成功！");
                        window.location.assign(this.base_url + "odoo/card")
                    }else{
                        console.log("支付失败！");
                        alert("支付失败");
                    }
                }
            );
        });
	},
});
var app = new BuyButton(null);

app.appendTo($(".o_buy")).then(function () {

    });
return BuyButton;
});


