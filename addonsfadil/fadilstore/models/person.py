from odoo import api, fields, models


class Person(models.Model):
    _name = 'fadilstore.person'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')

   
    
    
class Kasir(models.Model):
    _name = 'fadilstore.kasir'
    _inherit = 'fadilstore.person'
    _description = 'New Description'
    
    id_kasir = fields.Char(string='ID kasir')


    
    
class Cleaningservice(models.Model):
    _name = 'fadilstore.cleaningservice'
    _inherit = "fadilstore.person"
    _description = 'New Description'

    id_cln = fields.Char(string='ID Cleaning Service')
        
    
       
    
    
    
