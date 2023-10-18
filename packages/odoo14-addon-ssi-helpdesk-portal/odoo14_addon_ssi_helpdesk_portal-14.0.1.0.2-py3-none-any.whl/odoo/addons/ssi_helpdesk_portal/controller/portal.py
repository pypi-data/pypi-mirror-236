# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from operator import itemgetter

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv.expression import AND, OR
from odoo.tools import groupby as groupbyelem
from odoo.tools.translate import _

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        return values

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "ticket_count" in counters:
            values["ticket_count"] = (
                request.env["helpdesk_ticket"].search_count(
                    self._prepare_helpdesk_tickets_domain()
                )
                if request.env["helpdesk_ticket"].check_access_rights(
                    "read", raise_exception=False
                )
                else 0
            )
        return values

    def _prepare_helpdesk_tickets_domain(self):
        return [
            "|",
            "|",
            "|",
            ("partner_id", "=", request.env.user.partner_id.id),
            ("commercial_partner_id", "=", request.env.user.partner_id.id),
            ("additional_partner_ids", "in", request.env.user.partner_id.id),
            ("user_id", "=", request.env.user.id),
        ]

    def _ticket_get_page_view_values(self, ticket, access_token, **kwargs):
        values = {
            "page_name": "ticket",
            "ticket": ticket,
        }
        return self._get_page_view_values(
            ticket, access_token, values, "my_tickets_history", False, **kwargs
        )

    @http.route(
        ["/my/tickets", "/my/tickets/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def my_helpdesk_tickets(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby="all",
        search=None,
        groupby="none",
        search_in="content",
        **kw
    ):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_helpdesk_tickets_domain()

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "date desc"},
            "name": {"label": _("# Document"), "order": "name"},
            "state": {"label": _("State"), "order": "state"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
            "assigned": {"label": _("Assigned"), "domain": [("user_id", "!=", False)]},
            "unassigned": {
                "label": _("Unassigned"),
                "domain": [("user_id", "=", False)],
            },
            "open": {"label": _("In Progress"), "domain": [("state", "=", "open")]},
            "done": {"label": _("Done"), "domain": [("state", "=", "done")]},
        }
        searchbar_inputs = {
            "document": {"input": "document", "label": _("Search in # Document")},
            "title": {"input": "title", "label": _("Search in Title")},
            "contact": {"input": "contact", "label": _("Search in Contact")},
            "status": {"input": "status", "label": _("Search in Status")},
            "all": {"input": "all", "label": _("Search in All")},
        }
        searchbar_groupby = {
            "none": {"input": "none", "label": _("None")},
            "state": {"input": "state", "label": _("State")},
        }

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if filterby in ["last_message_sup", "last_message_cust"]:
            discussion_subtype_id = request.env.ref("mail.mt_comment").id
            messages = request.env["mail.message"].search_read(
                [
                    ("model", "=", "helpdesk_ticket"),
                    ("subtype_id", "=", discussion_subtype_id),
                ],
                fields=["res_id", "author_id"],
                order="date desc",
            )
            last_author_dict = {}
            for message in messages:
                if message["res_id"] not in last_author_dict:
                    last_author_dict[message["res_id"]] = message["author_id"][0]

            ticket_author_list = request.env["helpdesk_ticket"].search_read(
                fields=["id", "partner_id"]
            )
            ticket_author_dict = {
                ticket_author["id"]: ticket_author["partner_id"][0]
                if ticket_author["partner_id"]
                else False
                for ticket_author in ticket_author_list
            }

            last_message_cust = []
            last_message_sup = []
            ticket_ids = set(last_author_dict.keys()) & set(ticket_author_dict.keys())
            for ticket_id in ticket_ids:
                if last_author_dict[ticket_id] == ticket_author_dict[ticket_id]:
                    last_message_cust.append(ticket_id)
                else:
                    last_message_sup.append(ticket_id)

            if filterby == "last_message_cust":
                domain = AND([domain, [("id", "in", last_message_cust)]])
            else:
                domain = AND([domain, [("id", "in", last_message_sup)]])

        else:
            domain = AND([domain, searchbar_filters[filterby]["domain"]])

        if date_begin and date_end:
            domain = AND(
                [
                    domain,
                    [("create_date", ">", date_begin), ("create_date", "<=", date_end)],
                ]
            )

        # search
        if search and search_in:
            search_domain = []
            if search_in in ("document", "all"):
                search_domain = OR([search_domain, [("name", "ilike", search)]])
            if search_in in ("contact", "all"):
                search_domain = OR([search_domain, [("partner_id", "ilike", search)]])
            if search_in in ("title", "all"):
                search_domain = OR([search_domain, [("title", "ilike", search)]])
            if search_in in ("status", "all"):
                search_domain = OR([search_domain, [("state", "ilike", search)]])
            domain = AND([domain, search_domain])

        # pager
        tickets_count = len(request.env["helpdesk_ticket"].search(domain))
        pager = portal_pager(
            url="/my/tickets",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "search_in": search_in,
                "search": search,
                "groupby": groupby,
                "filterby": filterby,
            },
            total=tickets_count,
            page=page,
            step=self._items_per_page,
        )

        tickets = request.env["helpdesk_ticket"].search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_tickets_history"] = tickets.ids[:100]

        if groupby == "state":
            grouped_tickets = [
                request.env["helpdesk_ticket"].concat(*g)
                for k, g in groupbyelem(tickets, itemgetter("state"))
            ]
        else:
            grouped_tickets = [tickets]

        values.update(
            {
                "date": date_begin,
                "grouped_tickets": grouped_tickets,
                "page_name": "ticket",
                "default_url": "/my/tickets",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_filters": searchbar_filters,
                "searchbar_inputs": searchbar_inputs,
                "searchbar_groupby": searchbar_groupby,
                "sortby": sortby,
                "groupby": groupby,
                "search_in": search_in,
                "search": search,
                "filterby": filterby,
            }
        )
        return request.render("ssi_helpdesk_portal.portal_helpdesk_ticket", values)

    @http.route(
        [
            "/helpdesk/ticket/<int:ticket_id>",
            "/helpdesk/ticket/<int:ticket_id>/<access_token>",
            "/my/ticket/<int:ticket_id>",
            "/my/ticket/<int:ticket_id>/<access_token>",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def tickets_followup(self, ticket_id=None, access_token=None, **kw):
        try:
            ticket_sudo = self._document_check_access(
                "helpdesk_ticket", ticket_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ticket_get_page_view_values(ticket_sudo, access_token, **kw)
        return request.render("ssi_helpdesk_portal.tickets_followup", values)
