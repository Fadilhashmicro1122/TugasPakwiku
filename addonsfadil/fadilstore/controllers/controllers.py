from crypt import methods
from odoo import http, models, fields
from odoo.http import request
import json

class Fadilstore(http.Controller):
    @http.route('/fadilstore/getbarang', auth='public', method=["GET"])
    def getBarang(self, **kw):
        barang = request.env['fadilstore.barang'].search([])
        isi = []
        for bb in barang:
            isi.append({
                'nama_barang': bb.name,
                'harga_jua;': bb.harga_jual,
                'stok' : bb.stok

            })
        return json.dumps(isi)

    @http.route('/fadilstore/getsupplier', auth='public', method=["GET"])
    def getSupplier(self, **kw):
        supplier = request.env['fadilstore.suplier'].search([])
        sup = []
        for s in supplier:
            sup.append({
                'nama': s.name,
                'alamat': s.alamat,
                'no telfon': s.no_telp,
                'barang': s.barang_id[0].name
            })
        return json.dumps(sup)


