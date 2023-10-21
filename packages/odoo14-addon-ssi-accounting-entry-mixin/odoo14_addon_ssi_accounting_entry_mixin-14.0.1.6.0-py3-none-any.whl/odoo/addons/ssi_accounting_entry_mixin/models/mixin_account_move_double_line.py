# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MixinAccountMoveDoubleLine(models.AbstractModel):
    _name = "mixin.account_move_double_line"
    _description = "Accounting Move Double Line Mixin"

    _move_id_field_name = "move_id"

    # Debit ML Attribute
    _debit_account_id_field_name = "debit_account_id"
    _debit_partner_id_field_name = False
    _debit_analytic_account_id_field_name = False
    _debit_label_field_name = False
    _debit_product_id_field_name = False
    _debit_uom_id_field_name = False
    _debit_quantity_field_name = False
    _debit_price_unit_field_name = False
    _debit_currency_id_field_name = "currency_id"
    _debit_company_currency_id_field_name = "company_currency_id"
    _debit_amount_currency_field_name = "amount"
    _debit_company_id_field_name = "company_id"
    _debit_date_field_name = "date"
    _debit_need_date_due = False
    _debit_date_due_field_name = "date_due"

    # Credit ML Attribute
    _credit_account_id_field_name = "credit_account_id"
    _credit_partner_id_field_name = False
    _credit_analytic_account_id_field_name = False
    _credit_label_field_name = False
    _credit_product_id_field_name = False
    _credit_uom_id_field_name = False
    _credit_quantity_field_name = False
    _credit_price_unit_field_name = False
    _credit_currency_id_field_name = "currency_id"
    _credit_company_currency_id_field_name = "company_currency_id"
    _credit_amount_currency_field_name = "amount"
    _credit_company_id_field_name = "company_id"
    _credit_date_field_name = "date"
    _credit_need_date_due = False
    _credit_date_due_field_name = "date_due"

    def _create_standard_ml(self):
        self.ensure_one()
        ML = self.env["account.move.line"]
        debit_ml = ML.with_context(check_move_validity=False).create(
            self._prepare_standard_ml("debit")
        )
        credit_ml = ML.with_context(check_move_validity=False).create(
            self._prepare_standard_ml("credit")
        )
        return debit_ml, credit_ml

    def _prepare_standard_ml(self, direction):
        self.ensure_one()
        debit, credit, amount_currency = self._get_standard_amount(direction)
        partner = self._get_standard_partner(direction)
        aa = self._get_standard_aa(direction)
        move = self._get_standard_move()
        label = self._get_standard_label(direction)
        date_due = self._get_standard_date_due(direction)
        product = self._get_standard_product(direction)
        uom = self._get_standard_uom(direction)
        quantity = self._get_standard_quantity(direction)
        price_unit = self._get_standard_price_unit(direction)
        account = self._get_standard_account(direction)
        return {
            "move_id": move.id,
            "product_id": product and product.id or False,
            "product_uom_id": uom and uom.id or False,
            "quantity": quantity,
            "price_unit": price_unit,
            "name": label,
            "account_id": account and account.id or False,
            "debit": debit,
            "credit": credit,
            "currency_id": getattr(self, self._currency_id_field_name).id,
            "amount_currency": amount_currency,
            "partner_id": partner and partner.id or False,
            "analytic_account_id": aa and aa.id or False,
            "date_maturity": date_due,
        }

    def _get_standard_move(self):
        self.ensure_one()
        move = getattr(self, self._move_id_field_name)
        return move

    def _get_standard_account(self, direction):
        self.ensure_one()
        result = False
        if direction == "debit":
            if self._debit_account_id_field_name and hasattr(
                self, self._debit_account_id_field_name
            ):
                result = getattr(self, self._debit_account_id_field_name)
        elif direction == "credit":
            if self._credit_account_id_field_name and hasattr(
                self, self._credit_account_id_field_name
            ):
                result = getattr(self, self._credit_account_id_field_name)
        return result

    def _get_standard_product(self, direction):
        self.ensure_one()
        result = False
        if direction == "debit":
            if self._debit_product_id_field_name and hasattr(
                self, self._debit_product_id_field_name
            ):
                result = getattr(self, self._debit_product_id_field_name)
        elif direction == "credit":
            if self._credit_product_id_field_name and hasattr(
                self, self._credit_product_id_field_name
            ):
                result = getattr(self, self._credit_product_id_field_name)
        return result

    def _get_standard_partner(self, direction):
        self.ensure_one()
        result = False
        if direction == "debit":
            if self._debit_partner_id_field_name and hasattr(
                self, self._debit_partner_id_field_name
            ):
                result = getattr(self, self._debit_partner_id_field_name)
        elif direction == "credit":
            if self._credit_partner_id_field_name and hasattr(
                self, self._credit_partner_id_field_name
            ):
                result = getattr(self, self._credit_partner_id_field_name)

        return result

    def _get_standard_uom(self, direction):
        self.ensure_one()
        result = False
        if direction == "debit":
            if self._debit_uom_id_field_name and hasattr(
                self, self._debit_uom_id_field_name
            ):
                result = getattr(self, self._debit_uom_id_field_name)
        elif direction == "credit":
            if self._credit_uom_id_field_name and hasattr(
                self, self._credit_uom_id_field_name
            ):
                result = getattr(self, self._credit_uom_id_field_name)
        return result

    def _get_standard_quantity(self, direction):
        self.ensure_one()
        result = 0.0
        if direction == "debit":
            if self._debit_quantity_field_name and hasattr(
                self, self._debit_quantity_field_name
            ):
                result = getattr(self, self._debit_quantity_field_name)
        elif direction == "credit":
            if self._credit_quantity_field_name and hasattr(
                self, self._credit_quantity_field_name
            ):
                result = getattr(self, self._credit_quantity_field_name)
        return result

    def _get_standard_price_unit(self, direction):
        self.ensure_one()
        result = 0.0
        if direction == "debit":
            if self._debit_price_unit_field_name and hasattr(
                self, self._debit_price_unit_field_name
            ):
                result = getattr(self, self._debit_price_unit_field_name)
        elif direction == "credit":
            if self._credit_price_unit_field_name and hasattr(
                self, self._credit_price_unit_field_name
            ):
                result = getattr(self, self._credit_price_unit_field_name)
        return result

    def _get_standard_label(self, direction):
        self.ensure_one()
        result = False
        if direction == "debit":
            if self._debit_label_field_name and hasattr(
                self, self._debit_label_field_name
            ):
                result = getattr(self, self._debit_label_field_name)
        elif direction == "credit":
            if self._credit_label_field_name and hasattr(
                self, self._credit_label_field_name
            ):
                result = getattr(self, self._credit_label_field_name)
        return result

    def _get_standard_date_due(self, direction):
        self.ensure_one()
        result = False

        if direction == "debit":
            if not self._debit_need_date_due:
                return result

            if self._debit_date_due_field_name and hasattr(
                self, self._debit_date_due_field_name
            ):
                result = getattr(self, self._debit_date_due_field_name)

            if self._debit_need_date_due and not result:
                result = getattr(self, self._debit_accounting_date_field_name)
        elif direction == "credit":
            if not self._credit_need_date_due:
                return result

            if self._credit_date_due_field_name and hasattr(
                self, self._credit_date_due_field_name
            ):
                result = getattr(self, self._credit_date_due_field_name)

            if self._credit_need_date_due and not result:
                result = getattr(self, self._credit_accounting_date_field_name)
        return result

    def _get_standard_aa(self, direction):
        self.ensure_one()
        result = False
        if direction == "debit":
            if self._debit_analytic_account_id_field_name and hasattr(
                self, self._debit_analytic_account_id_field_name
            ):
                result = getattr(self, self._analytic_account_id_field_name)
        elif direction == "credit":
            if self._credit_analytic_account_id_field_name and hasattr(
                self, self._credit_analytic_account_id_field_name
            ):
                result = getattr(self, self._credit_analytic_account_id_field_name)
        return result

    def _get_standard_amount(self, direction):
        self.ensure_one()
        debit = credit = amount = 0.0
        if direction == "debit":
            amount_currency = getattr(self, self._debit_amount_currency_field_name)
            currency = getattr(self, self._debit_currency_id_field_name)
            company_currency = getattr(self, self._debit_company_currency_id_field_name)
        elif direction == "credit":
            amount_currency = getattr(self, self._credit_amount_currency_field_name)
            currency = getattr(self, self._credit_currency_id_field_name)
            company_currency = getattr(
                self, self._credit_company_currency_id_field_name
            )

        amount = currency.compute(
            abs(amount_currency),
            company_currency,
        )

        if direction == "debit" and amount_currency > 0:
            debit = amount
        elif direction == "debit" and amount_currency < 0:
            credit = amount
        elif direction == "credit" and amount_currency > 0:
            credit = amount
            amount_currency *= -1
        elif direction == "credit" and amount_currency < 0:
            debit = amount
            amount_currency *= -1

        return debit, credit, amount_currency
