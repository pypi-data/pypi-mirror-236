odoo.define("ssi_helpdesk_portal.menu", function (require) {
"use strict";

var publicWidget = require('web.public.widget');

publicWidget.registry.HelpdeskMenu = publicWidget.Widget.extend({
    selector: '.ticket_menu',

    /**
     * @override
     */
    start: function () {
        var pathname = $(window.location).attr("pathname");
        var $links = this.$('li a');
        if (pathname !== "/helpdesk/") {
            $links = $links.filter("[href$='" + pathname + "']");
        }
        $links.first().closest("li").addClass("active");

        return this._super.apply(this, arguments);
    },
});
});
