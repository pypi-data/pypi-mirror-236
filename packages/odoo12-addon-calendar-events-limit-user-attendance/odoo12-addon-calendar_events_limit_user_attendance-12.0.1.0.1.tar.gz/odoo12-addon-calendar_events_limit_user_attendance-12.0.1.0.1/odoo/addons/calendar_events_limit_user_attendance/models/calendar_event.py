from odoo import models, api, fields

class Meeting(models.Model):
    _inherit = 'calendar.event'

    user_partner_ids = fields.Many2many(
        "res_partner",
        compute="_compute_user_partner_ids",
    )

    @api.depends("user_id")
    def _compute_user_partner_ids(self):
        users = self.env["res.users"].search([("active", "=", True)])

        for calendar_event in self:
            calendar_event.user_partner_ids = [
                (6, 0, users.mapped("partner_id").ids)
            ]
