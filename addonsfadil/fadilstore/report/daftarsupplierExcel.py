from odoo import models, fields

class PartnerXlsx(models.AbstractModel):
    _name = 'report.fadilstore.report_suplier_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    tgl_lap = fields.Date.today()
    
    def generate_xlsx_report(self, workbook, data, supplier):
        sheet = workbook.add_worksheet('Daftar Supplier')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.tgl_lap))
        sheet.write(1, 0, 'NAMA PERUSAHAAN', bold)
        sheet.write(1, 1, 'ALAMAT', bold)
        sheet.write(1, 2, 'NO TELPON', bold)
        sheet.write(1, 3, 'PRODUK', bold)
        row = 2
        col = 1
        for obj in supplier:
            sheet.write(row, col+1, obj.name)
            sheet.write(row, col+1, obj.alamat)
            sheet.write(row, col+2, obj.no_telp)
            for xxx in obj.barang_id:
                 sheet.write(row, col+3, xxx.name)
                 col += 1
            row += 1