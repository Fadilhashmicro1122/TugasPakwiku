from odoo import api, fields, models


class KelompokBarang(models.Model):
    _name = 'fadilstore.kelompokbarang'
    _description = 'New Description'
    _rec_name = 'nama'
    
    nama = fields.Selection([('makananbasah', 'Makanan Basah'), ('makanankering', 'Makanan Kering'),('minuman', 'Minuman')], string='Kelompok Barang') 
    kode_kelompok = fields.Char(string='Kode Kelompok')
    kode_rak = fields.Char(string='Kode Rak')
    barang_ids = fields.One2many(comodel_name='fadilstore.barang', inverse_name='kelompokbarang_id', string='Daftar Barang')
    jml_item = fields.Char(compute='_compute_jml_item', string='jumlah item')
    daftar = fields.Char(string='Daftar Isi')

    @api.onchange('nama')
    def _compute_kode_kelompok(self):
        if (self.nama == 'makananbasah'):
            self.kode_kelompok = 'mak01'
        elif (self.nama == 'makanankering'):
              self.kode_kelompok = 'mak02'
        elif (self.nama == 'minuman'):
              self.kode_kelompok = 'min01'

    @api.depends('barang_ids')
    def _compute_jml_item(self):
        for rec in self: 
            a = self.env['fadilstore.barang'].search([('kelompokbarang_id', '=', rec.id)]).mapped('name')
            b = len(a)
            rec.jml_item = b
            rec.daftar = a  
    
    