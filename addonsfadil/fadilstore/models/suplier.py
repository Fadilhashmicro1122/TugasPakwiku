from odoo import api, fields, models


class Suplier(models.Model):
    _name = 'fadilstore.suplier'
    _description = 'New Description'
    
    name = fields.Char(string='Name')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='No Telpon')
    barang_id = fields.Many2many(comodel_name='fadilstore.barang', string='Barang')
    
    
    
