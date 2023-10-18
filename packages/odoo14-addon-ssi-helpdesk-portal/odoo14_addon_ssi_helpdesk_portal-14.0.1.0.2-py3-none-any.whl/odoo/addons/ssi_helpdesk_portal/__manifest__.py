# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
{
    "name": "Helpdesk Portal",
    "version": "14.0.1.0.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "utm",
        "portal",
        "website",
        "website_form",
        "ssi_helpdesk",
    ],
    "data": [
        "data/website_helpdesk.xml",
        "views/assets.xml",
        "views/helpdesk_templates.xml",
        "views/helpdesk_portal_templates.xml",
    ],
    "demo": [],
    "images": [],
}
