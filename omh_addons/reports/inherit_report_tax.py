from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTax(models.AbstractModel):
    _inherit = 'report.base_accounting_kit.report_tax'
    _description = 'Tax Report'

    def _sql_from_amls_one(self):
        sql = """SELECT "account_move_line".tax_line_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0), COALESCE(SUM("account_move_line".tax_base_amount), 0)
                    FROM %s
                    WHERE %s  GROUP BY "account_move_line".tax_line_id"""
        return sql



    def _compute_from_amls(self, options, taxes):
        # in this method, we compute the total amounts of the taxes and net ammount.
        sql = self._sql_from_amls_one()
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()

        query = sql % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        print("--------- ##################### query #####################  ----------------------", query )

        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['tax'] = abs(result[1])
                taxes[result[0]]['net'] = abs(result[2])
                print("--------- ##################### result 90909090#####################  ----------------------", result, taxes[result[0]] )
    