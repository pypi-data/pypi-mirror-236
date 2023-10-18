# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

import base64

from odoo import api, models

from odoo.addons.http_routing.models.ir_http import slug


class HelpdeskTicket(models.Model):
    _name = "helpdesk_ticket"
    _inherit = [
        "helpdesk_ticket",
        "portal.mixin",
        "mail.thread.cc",
        "utm.mixin",
        "rating.mixin",
        "mail.activity.mixin",
        "website.published.mixin",
    ]

    def get_helpdesk_url(self):
        self.ensure_one()
        return "/helpdesk/%s" % slug(self)

    @api.model
    def create(self, values):
        if self.env.context.get("from_website"):
            context = self.env.context
            values.update(
                {
                    "title": context["title"],
                    "partner_id": context["partner_id"],
                    "user_id": context["user_id"],
                    "description": context.get("description"),
                }
            )
        res = super(HelpdeskTicket, self).create(values)
        if self.env.context.get("from_website"):
            attachment_ids = []
            for attachment in values.get("attachments", []):
                file_name = attachment.filename
                file = attachment.read()
                attachment_id = (
                    self.env["ir.attachment"]
                    .sudo()
                    .create(
                        {
                            "name": file_name,
                            "type": "binary",
                            "datas": base64.b64encode(file),
                            "res_model": res._name,
                            "res_id": res.id,
                        }
                    )
                )
                attachment_ids.append(attachment_id.id)
            if attachment_ids:
                res.message_post(attachment_ids=attachment_ids)
        return res
