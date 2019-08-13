odoo.define('juan_tong.button_share', function(require){
'use strict';
var core = require('web.core');

var Widget = require('web.Widget');
var User = require('juantong.share').Ticket;

var ajax = require('web.ajax');
var qweb = core.qweb;
var _t = core._t;

require('web.dom_ready');
var ShareButton = Widget.extend({
    template: 'share.template',
    events: {
        'click .o_share_a': '_onClick',
    },
    xmlDependencies: ['/juan_tong/static/src/xml/widget_template.xml'],

    init: function () {

    },
    _onClick: function () {

        alert('159');
        this.user = new User();

        var c = this.user.test();
        /*console.log(typeof(c));
        alert(typeof(c));
        alert(JSON.stringify(c));*/
        },
});
var app = new ShareButton(null);
app.appendTo($(".o_share")).then(function () {

    });
//core.action_registry.add('demo',Counter);
return ShareButton;
});

