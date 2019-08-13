odoo.define('juantong.share', function (require) {
'use strict';

var Class = require('web.Class');
var rpc = require('web.rpc');
var session = require('web.Session');
var Ticket = Class.extend({

    init:function(){

       /*this.b = this._rpc({
            model:'shangjia',
            method:'button_check_test5',
            args:[[]
                ]
        });
        alert(this.b);
        alert(JSON.stringify(this.b));

        var a = rpc.query({
            model:'shangjia',
            method:'button_check_test5',
            args:[[]
                ]
        });
        alert(a.appId);
        return a.then(function(a){

            alert(a.appId);
            console.log('调用py成功');
            alert(JSON.stringify(a));
            //window.location.href = a;
        })*/

        },

    test: function(){
        /*var self = this;
        var b = rpc.query({
            model:'shangjia',
            method:'button_check_test5',
            args:[[]
                ]
        });
        alert("p1"+JSON.stringify(b));
        this.b = b;
        return b.then(function(b){
            console.log('调用py成功');
            alert("p2"+JSON.stringify(b));
            this.c = b;

        })*/
	alert('function test');
        },

    onBridgeReady: function(){

	    var self = this;
       var b = rpc.query({
            model:'shangjia',
            method:'button_check_test5',
            args:[[]
                ]
        }).then(function(b){

        alert("p1"+JSON.stringify(b));
       
        alert("p3"+JSON.stringify(b.appId));
        WeixinJSBridge.invoke(
         'getBrandWCPayRequest', {
         "appId":b.appId,     //公众号名称，由商户传入
         "timeStamp":b.timeStamp,         //时间戳，自1970年以来的秒数
         "nonceStr":b.nonceStr, //随机串
         "package":b.package,
         },


      function(res){
      if(res.err_msg == "get_brand_wcpay_request:ok" ){
      // 使用以上方式判断前端返回,微信团队郑重提示：
            //res.err_msg将在用户支付成功后返回ok，但并不保证它绝对可靠。
      	alert('success');
	}
   });
})
},
    });
return {
    Ticket:Ticket,
};
});



