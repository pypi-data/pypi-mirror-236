# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import http
from odoo.http import request

from odoo.addons.website_form.controllers.main import WebsiteForm


class HelpdeskPortal(http.Controller):
    @http.route(
        ["/helpdesk/", '/helpdesk/<model("helpdesk_ticket"):ticket>'],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def ssi_helpdesk_portal(self, ticket=None, **kwargs):
        kwargs.get("search")
        # For breadcrumb index: get all ticket
        tickets = request.env["helpdesk_ticket"].search([], order="id asc")
        result = {"ticket": ticket}
        # For breadcrumb index: get all ticket
        result["tickets"] = tickets
        return request.render("ssi_helpdesk_portal.ticket", result)


class WebsiteForm(WebsiteForm):
    def _handle_website_form(self, model_name, **kwargs):
        context = request.env.context.copy()
        attachments = []
        for key, value in kwargs.items():
            if key[:11] == "attachments":
                attachments.append(value)
        values = {
            "from_website": True,
            "title": kwargs.get("title"),
            "partner_id": request.env.user.partner_id.id,
            "user_id": request.env.ref("base.user_admin").id,
            "description": kwargs.get("description"),
            "attachments": attachments,
        }
        context.update(values)
        request.env.context = context
        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
