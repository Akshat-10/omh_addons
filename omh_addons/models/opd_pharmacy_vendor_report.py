from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class OpdPharmacyVendorReport(models.Model):
    _name = 'opd.pharmacy.vendor.report'
    _description = "OPD Pharmacy Vendor Report"


    name = fields.Char()

    partner_ids = fields.Many2many('res.partner', string="Vendor")

    payment_type = fields.Selection([
        ('paid','Paid'),
        ('not_paid', 'Not Paid'),
        ('partial','Partial Paid'),
        ('all','All')
    ], string="Payment Type", default='all')

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)


    @api.model
    def create(self, vals):
        if vals.get('from_date') and vals.get('to_date'):
            from_date = datetime.strptime(vals['from_date'], '%Y-%m-%d').date()
            to_date = datetime.strptime(vals['to_date'], '%Y-%m-%d').date()
            if from_date > to_date:
                raise ValidationError("From Date cannot be greater than To Date")
            if from_date > datetime.today().date():
                raise ValidationError("From Date cannot be greater than today's date")
        return super(OpdPharmacyVendorReport, self).create(vals)

    def write(self, vals):
        if vals.get('from_date') or vals.get('to_date'):
            from_date = vals.get('from_date', self.from_date)
            to_date = vals.get('to_date', self.to_date)
            if from_date and to_date:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
                if from_date > to_date:
                    raise ValidationError("From Date cannot be greater than To Date")
                if from_date > datetime.today().date():
                    raise ValidationError("From Date cannot be greater than today's date")
        return super(OpdPharmacyVendorReport, self).write(vals)


    def opd_pharmacy_vendor_action(self):
        print("---- Button is clicked -----------", self.from_date, self.to_date, self.partner_ids, self.payment_type)
        

        domain = [('invoice_date','>=', self.from_date),('invoice_date','<=', self.to_date),('move_type','=','in_invoice'),('warehouse_id', '=', 14)]

        if self.partner_ids:
            domain.append(('partner_id','in', self.partner_ids.ids))

        if self.payment_type != 'all':
            domain.append(('payment_state','=', self.payment_type))


        bill_ids = self.env['account.move'].search(domain=domain)

        # for ab in bill_ids:
        #     print('00000000000000000000',"name - ",ab.partner_id.name," invoice date - ",ab.invoice_date,"bank ka naam - ",ab.partner_id.bank_ids[0].bank_id.name,"Bnak account number - ",ab.partner_id.bank_ids[0].acc_number,"Amount - ",-ab.amount_total_signed,"Payment Type - ",ab.payment_state)
        # # 123yyuiy
        data = {
            'bill_ids': bill_ids.ids,
            'form_data': self.read()[0],
        }
        return self.env.ref('omh_addons.opd_pharmacy_vendor_xls_report_custom').report_action(self, data=data)
    

