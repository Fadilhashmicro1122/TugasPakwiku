from odoo import api, fields, models


class LaporanKeuangan(models.Model):
    _name = 'fadilstore.laporanlaba'
    _description = 'New Description'
    
    name = fields.Char(string="name")
    barang_id = fields.Many2one(comodel_name='fadilstore.barang', string='Laba')
    tgl_laporanlaba = fields.Datetime(string='Tanggal Transaksi',default = fields.Datetime.now())
    laporantotal_laba = fields.Integer(string='Subtotal Laba')
    penjualan_ids = fields.One2many(comodel_name='fadilstore.penjualan',inverse_name='laporanlaba_id',string='laporan laba')
    partner_id = fields.Many2one('res.partner', string="Customer")
    laporan_laba_ids = fields.One2many('fadilstore.laporanlaba.line','laporan_laba_id',string='laporan laba')
    source_document = fields.Char(string='Source Document')



class LaporanKeuanganLine(models.Model):
    _name = 'fadilstore.laporanlaba.line'
    _description = 'fadilstore.laporanlaba.line'
    
    name = fields.Char(string="name")
    laporan_laba_id = fields.Many2one('fadilstore.laporanlaba', string='laporan laba id')
    product_id = fields.Many2one('fadilstore.barang', string="Product")
    qty = fields.Integer(string='Quantity')
    unit_price = fields.Integer(string='Harga Jual')
    

   

    
    
  

    # @api.onchange('penjualan_ids')
    # def _compute_laporantotal_laba(self):
    #     if (self.penjualan_ids.laba):
    #         self.laporantotal_laba = self.penjualan_ids.laba
          

   
   
    
    
    
