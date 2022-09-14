from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

 
class Penjualan(models.Model):
    _name = 'fadilstore.penjualan'
    _description = 'New Description'

    name = fields.Char(string='No Nota')
    nama_pembeli = fields.Char(string='Nama Pembeli')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    tgl_penjualan = fields.Datetime(string='Tanggal Transaksi',default = fields.Datetime.now())
    laba_bersih = fields.Integer(compute="_compute_lababersih",string='Laba Bersih')
    total_bayar = fields.Integer(compute='_compute_totalbayar',string='Total Pembayaran')
    detailpenjualan_ids = fields.One2many(comodel_name='fadilstore.detailpenjualan',inverse_name='penjualan_id',string='Detail Penjualan')
    laporanlaba_id = fields.Many2one(comodel_name='fadilstore.laporanlaba',string='Laporan Laba')
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('confirm', 'Confirm')], required=True, readonly=True, default='draft')
    uang_masuk = fields.Integer(string='Inputkan Uang Masuk')
    uang_kembalian = fields.Integer(compute='_compute_kembalian',string='Kembalian')
    
    
    
    def action_confirm(self):
        prepare_laba_line = []
        for line in self.detailpenjualan_ids:
            prepare_laba_line.append((0,0, {
                'name': 'line',
                'product_id': line.barang_id.id,
                'qty': line.qty,
                'unit_price': line.harga_satuan
            }))
            
        laba = {
            'name': 'Subtotal Laba',
            'source_document': self.name,
            'tgl_laporanlaba': self.tgl_penjualan,
            'laporantotal_laba' : self.laba_bersih,
            'partner_id' : self.partner_id.id,
            'laporan_laba_ids' : prepare_laba_line

        }
        keuangan = self.env['fadilstore.laporanlaba'].create(laba)
        self.write({'state':'confirm'})
    



    @api.depends('uang_masuk', 'total_bayar')
    def _compute_kembalian(self):
        for rec in self:
            rec.uang_kembalian = rec.uang_masuk - rec.total_bayar

    def action_settodraft(self):
        self.write({'state':'draft'})


    @api.depends('detailpenjualan_ids')
    def _compute_totalbayar(self):
        for rec in self:
            a = sum(self.env['fadilstore.detailpenjualan'].search([('penjualan_id','=',rec.id)]).mapped('subtotal_hargajual'))
            rec.total_bayar = a
    
    @api.depends('detailpenjualan_ids')
    def _compute_lababersih(self):
        for rec in self:
            l = sum(self.env['fadilstore.detailpenjualan'].search([('penjualan_id', '=',rec.id)]).mapped('laba'))
            rec.laba_bersih = l
    
    @api.ondelete(at_uninstall=False)
    def _ondelete_penjualan(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError("Status Confirm Data Tidak Dapat Dihapus")
        else:
            if self.detailpenjualan_ids:
                a=[]
                for rec in self:
                    a = self.env['fadilstore.detailpenjualan'].search([('penjualan_id','=',rec.id)])
                    print(a)
                for ob in a:
                    print(str(ob.barang_id.name)+' '+str(ob.qty))
                    ob.barang_id.stok += ob.qty
    
    def write(self,vals):
        for rec in self:
            a = self.env['fadilstore.detailpenjualan'].search([('penjualan_id', '=', rec.id)])
            print(a)
            for data in a:
                print(str(data.barang_id.name)+' '+str(data.qty)+' '+str(data.barang_id.stok))
                data.barang_id.stok += data.qty 
        record = super(Penjualan,self).write(vals)
        for rec in self:
            b = self.env['fadilstore.detailpenjualan'].search([('penjualan_id', '=', rec.id)])
            print(a)
            print(b)
            for databaru in b:
                if databaru in a:
                    print(str(databaru.barang_id.name)+' '+str(databaru.qty)+' '+str(databaru.barang_id.stok))
                    databaru.barang_id.stok -= databaru.qty
                else:
                    pass 

        return record
        
    
    _sql_constraints = [
        ('no_nota_unik','unique (name)','No Nota Sudah Di Gunakan!!!')
    ]

class DetailPenjualan(models.Model):
    _name = 'fadilstore.detailpenjualan'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(comodel_name='fadilstore.penjualan',string='Detail Penjualan')
    barang_id = fields.Many2one(comodel_name='fadilstore.barang',string='List Barang')
    harga_satuan = fields.Integer(string='Harga Jual')
    harga_modal = fields.Integer(string='Harga Modal')
    qty = fields.Integer(string='Quantity')
    subtotal_hargajual = fields.Integer(compute='_compute_subtotal',string='Subtotal Harga Jual')
    subtotal_hargamodal = fields.Integer(compute='_compute_subtotal_hargamodal',string='Subtotal Harga Beli')
    laba = fields.Integer(compute='_compute_laba',string='Laba')
    laporanlaba_id = fields.Many2one(comodel_name='fadilstore.laporanlaba', string='Laporan Laba')
    
    @api.onchange('barang_id')
    def _onchange_(self):
        if (self.barang_id.harga_jual):
            self.harga_satuan = self.barang_id.harga_jual

    @api.onchange('barang_id') 
    def _compute_hargamodalsatuan(self):
        if (self.barang_id.harga_beli):
            self.harga_modal = self.barang_id.harga_beli

    @api.depends('harga_modal', 'qty')
    def _compute_subtotal_hargamodal(self):
        for rec in self:
            rec.subtotal_hargamodal = rec.qty * rec.harga_modal
    
    @api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal_hargajual = rec.qty * rec.harga_satuan

    @api.depends('subtotal_hargajual','subtotal_hargamodal')
    def _compute_laba(self):
        for rec in self:
            rec.laba = rec.subtotal_hargajual - rec.subtotal_hargamodal
            
    @api.model
    def create(self,vals):
        record = super(DetailPenjualan,self).create(vals)
        if record.qty:
            self.env['fadilstore.barang'].search([('id',"=",record.barang_id.id)]).write({'stok': record.barang_id.stok - record.qty})
        return record 
    
    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty <1:
                raise ValidationError("Silahkan Masukan Jumlah Pembelian Pada Barang {}".format(rec.barang_id.name))
            elif rec.barang_id.stok < rec.qty: 
                raise ValidationError("Jumlah Pembelian {} Melebihi Batas, Stok Yang Tersedia Hanya {}".format(rec.barang_id.name,rec.barang_id.stok))
    
    

    
    

    
