# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyInterventionType(models.Model):
    _name = "psychology_intervention_type"
    _description = "Psychology Intervention Type"
    _inherit = [
        "mixin.master_data",
    ]
    allowed_facilitator_ids = fields.Many2many(
        comodel_name="res.users",
        string="Allowed Facilitators",
        relation="rel_psychology_intervention_type_2_facilitator",
        column1="type_id",
        column2="user_id",
    )
