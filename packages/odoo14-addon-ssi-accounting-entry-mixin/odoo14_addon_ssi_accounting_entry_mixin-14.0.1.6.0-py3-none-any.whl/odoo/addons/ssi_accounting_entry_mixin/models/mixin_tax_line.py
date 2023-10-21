# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinTaxLine(models.AbstractModel):
    _name = "mixin.tax_line"
    _description = "Tax Line Mixin"
    _inherit = [
        "mixin.account_move_single_line",
    ]

    _analytic_account_id_field_name = "analytic_account_id"
    _label_field_name = "name"
    _amount_currency_field_name = "tax_amount"

    name = fields.Char(
        string="Description",
        required=True,
    )
    tax_id = fields.Many2one(
        string="Tax",
        comodel_name="account.tax",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
    )
    base_amount = fields.Monetary(
        string="Base Amount",
        currency_field="currency_id",
        required=True,
    )
    tax_amount = fields.Monetary(
        string="Tax Amount",
        currency_field="currency_id",
        required=True,
    )
    manual = fields.Boolean(
        string="Manual",
        default=True,
    )
    move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
    )
