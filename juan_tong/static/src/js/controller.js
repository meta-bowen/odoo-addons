odoo.define('juan_tong.demo', function(require){
'use strict';
var core = require('web.core');
//var session = require('web.Session');
//var Dialog = require('web.Dialog');
//var notification = require('web.notification');
//var User = require('juantong.share').Ticket;
var Widget = require('web.Widget');
var User = require('juantong.share').Ticket;
//var Router = require('demo.router');
var ajax = require('web.ajax');
var qweb = core.qweb;
var _t = core._t;

require('web.dom_ready');
var Counter = Widget.extend({
    template: 'some.template',
    events: {
        'click .o_juantong_get_token': '_onClick',
    },
    xmlDependencies: ['/juan_tong/static/src/xml/ticket_views.xml'],

    init: function () {


    },
    _onClick: function () {
        this.user = new User();

        var c = this.user.test();
        alert('158');
        var d = onBridgeReady();
        alert('123');
        /*if (typeof WeixinJSBridge == "undefined") {
            if (document.addEventListener) {
                document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
            } else if (document.attachEvent) {
                document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
                document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
            }
        } else {
            onBridgeReady();
        }*/
        },
    onBridgeReady: function(){
        alert('支付接口函数');
    }
});
console.log('777');
//var $elem = $('#o_juantong_get');
var app = new Counter(null);
console.log('test');
app.appendTo($(".o_juantong_get")).then(function () {



    });
//core.action_registry.add('demo',Counter);
return Counter;
});