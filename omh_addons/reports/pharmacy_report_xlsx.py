from odoo import models, _


class OmhPharmacyReportXlsx(models.AbstractModel):
    _name = 'report.omh_addons.pharmacy_report_custom_xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, partners):
        print("-------- Printing an Excel Report -----------", data)
        for d in data:
            print("-------- Printing an Excel Report00000000 -----------", d, '=====', data[d])


        sheet = workbook.add_worksheet('OPD Pharmacy Vendor Report')
        bold = workbook.add_format({'bold': True})
        # sheet.set_column('C:C', 20)
        # sheet.set_column('D:D', 15)
        # sheet.set_column('E:E', 15)
        # sheet.set_column('F:F', 15)
        # sheet.set_column('G:G', 15)
        # sheet.set_column('H:H', 15)
        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 30)
        # sheet.set_column('F:F', 30)

        row = 0
        col = 0
        sheet.write(row, col, 'Vendor Name', bold)
        sheet.write(row, col + 1, 'Bank Name', bold)
        sheet.write(row, col + 2, 'Account Number', bold)
        sheet.write(row, col + 3, 'Amount', bold)
        sheet.write(row, col + 4, 'Payment Status', bold)

        vendor_totals = {}
        # paid = []
        # not_paid = []
        # partial = []

        for bill in data['bill_ids']:
            bill_id = self.env['account.move'].browse(bill)
            vendor_name = bill_id.partner_id.name
            payment_status = bill_id.payment_state
            partner = bill_id.partner_id.id
            warehouse = bill_id.warehouse_id.name

            bank_name = ''
            account_number = ''

            bank_ids = bill_id.partner_id.bank_ids
            if bank_ids:
                bank_name = bank_ids[0].bank_id.name
                account_number = bank_ids[0].acc_number

            total_amount = -bill_id.amount_total_signed

            # if payment_status == 'paid':
            #     paid.append(bill_id.id)
            # elif payment_status == 'not_paid':
            #     not_paid.append(bill_id.id)
            # else:
            #     partial.append(bill_id.id)

            if (vendor_name, payment_status, bank_name, account_number, partner) in vendor_totals:
                vendor_totals[(vendor_name, payment_status, bank_name, account_number, partner )] += total_amount
            else:
                vendor_totals[(vendor_name, payment_status, bank_name, account_number, partner)] = total_amount
            print("-----------vendor total-------------------", vendor_totals )
            print("--------------------------93712037219073902173902174-----", bill_id, vendor_name,bank_ids, bank_name, account_number, total_amount, payment_status, warehouse)

        
        for vendor_status, total_amount in  sorted(vendor_totals.items()):
            print("!!!!!!!!!!!! vendor status-!!!!!!!!!!!!!!!!!", vendor_status, total_amount)
            vendor_name, payment_status, bank_name, account_number, partner = vendor_status
            row += 1
            # sheet.write(row, col - 1, partner, bold)
            sheet.write(row, col, vendor_name, bold)

            sheet.write(row, col + 1, bank_name)
            sheet.write(row, col + 2, account_number)

            sheet.write(row, col + 3, total_amount)
            sheet.write(row, col + 4, payment_status)
            # if payment_status == 'paid':
            #     sheet.write(row, col + 5, str(paid))
            # elif payment_status == 'not_paid':
            #     sheet.write(row, col + 5, str(not_paid))
            # else:
            #     sheet.write(row, col + 5, str(partial))

        workbook.close()






        # for bill in data['bill_ids']:
        #     bill_id = self.env['account.move'].browse(bill)
        #     print(" 44444=-------------- ",bill_id, "hewfuiuhewuufho 99999999999999-------------------")
        #     row += 1
        #     sheet.write(row, col, bill_id.partner_id.name, bold)
        #     if bill_id.partner_id.bank_ids and bill_id.partner_id.bank_ids[0]:
        #         sheet.write(row, col + 1, bill_id.partner_id.bank_ids[0].bank_id.name)
        #         sheet.write(row, col + 2, bill_id.partner_id.bank_ids[0].acc_number)
        #     else:
        #         sheet.write(row, col + 1, '')
        #         sheet.write(row, col + 2, '')

        #     sheet.write(row, col + 4, -bill_id.amount_total_signed, bold)
        #     sheet.write(row, col + 5, bill_id.payment_state, bold)
        

        # workbook.close()

