# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm

###### HERENCIA A LINEAS DEL PEDIDO #######
class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit ='sale.order.line'
    _columns = {
        'date_arranged': fields.date('Promesa Entrega', required=True),
        'ship_to': fields.selection(
            (('CEDIS','CEDIS'),('TYP_HMO','Tienda Hermosillo'),('TYP_OBG','Tienda Obregon'),
             ('TYP_CLN','Tienda Culiacan'),('TYP_GDL','Tienda Guadalajara'),('TYP_LPZ','Tienda La Paz'),
             ('TYP_LMS','Tienda Los Mochis'),('TYP_MXL','Tienda Mexicali'),('TYP_NGZ','Tienda Nogales'),
             ('TYP_TJ','Tienda Tijuana')),'Envio a Tienda:'),
        'imported':fields.boolean('Importacion', help="Marcar si es producto importado"),
        'partial_supply':fields.boolean('surtir parcial'), 
        'ship_invoiced':fields.boolean('Facturar Flete'),
        'special_ship': fields.text('Embarque Especial', help="ATENCION A:\nDIRECCION:\nCOLONIA:\nC.P.:\nTELEFONO:\nCIUDAD:\nRFC:"),
        'change_address': fields.boolean('cambiar direccion embarque',help="Marcar esta opcion si se va cambiar la direccion de embarque"),
        'supplier_id': fields.many2one('res.partner','Proveedor'),
        'import_type': fields.selection((('Semanal','semanal'),('Express','express'),),'Tipo de importacion:'),
        'broker': fields.char('Agencia', size=60),
        'carrier': fields.char('Fletera', size=60),
        'arrange': fields.char('Compromisos de Venta', size=128 , help="Llenar con los acuerdos en caso de haber un precio pactado o descuento"),

        }
    _defaults = {}
    # def _validar_campos(self,cr,uid,ids,context=None):
    #     record = self.browse(cr,uid,ids,context=context)[0]
    #     for rec in record:
    #         if rec.ship_to and rec.special_ship:
    #             return True
    #         return False
    # _constraints = [(_validar_campos,'Error o es a tienda u otra direccion',['special_ship'])],
###### HERENCIA DE PEDIDO DE VENTA #######
class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit ='sale.order'
    _columns = {
        'special_sale_global': fields.boolean('Venta Especial'),
        'special_ship_global': fields.text('Embarque Especial', help="Llenar Solamente cuando todos los produtos vayan a la misma direccion"),
        'create_uid': fields.many2one('res.users','Usuario',readonly=1),
        }
    _defaults = {
        # 'special_ship_global': "ATENCION A:\nDIRECCION:\nCOLONIA:\nC.P.:\nTELEFONO:\nCIUDAD:\nRFC:",
    }
    ######## HERENCIA AL METODO CONFIRMAR PEDIDO DE VENTA ######
    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_button_confirm(cr, uid, ids,
         context)
        print "############## CONFIRMANDO PEDIDO DE VENTA >>>> "
        print "############## CONFIRMANDO PEDIDO DE VENTA >>>> "
        purchase_obj = self.pool.get('purchase.order')
        self_br = self.browse(cr, uid, ids, context=None)[0]
        print "##################### SELF BR >>>> ", self_br
        print "##################### SELF BR >>>> ", self_br.name
        print "##################### SELF BR >>>> ", self_br.pricelist_id.name

        purchase_ids = purchase_obj.search(cr, uid, 
            [('origin','=',self_br.name)])
        # cr.execute("""select id from purchase_order 
        #     where origin ='%s' """ % (self_br.name,))
        # sql_cr = cr.fetchall()
        # print "############# RESULTADO DE QUERY SQL >>>> ",sql_cr
        print "#################### PURCHASE IDS >>>>>> ", purchase_ids
        ###### BUSCANDO PEDIDOS DE COMPRA LIGADOS A VENTA #####
        purchase_line_obj = self.pool.get('purchase.order.line')
        if purchase_ids:
            for line in self_br.order_line:
                if line.type == 'make_to_order':
                    purchase_line_ids = purchase_line_obj.search(cr, uid,
                        [('product_id','=',line.product_id.id),
                        ('order_id','in',tuple(purchase_ids))])
                    if purchase_line_ids:
                        purchase_line_obj.write(cr, uid, purchase_line_ids,
                             {
                             'special_sale': line.special_sale,
                              'ref_customer': line.ref_customer,
                              'supplier': line.supplier,
                              })
                    ### EQUIVALENTE A CODIGO SQL ###
                    # cr.execute("""update purchase_order_line set 
                    #     special_sale=%s,
                    #     ref_customer=%s where id in %s;
                    #     """, (line.special_sale, line.ref_customer, 
                    #         tuple(purchase_line_ids)))

        return res
        
## HERENCIA DE PARTNER PARA SELECCIONAR PROVEEDORES
class partner_asignment(osv.osv):
    _name = 'res.partner'
    _inherit ='res.partner'
    _columns = {
       'supplier_id': fields.one2many('sale.order.line','supplier_id','Proveedor'),
        }
    ###### HERENCIA A LINEAS DEL COMPRA #######    
class purchase_order_line(osv.osv):
    _name = 'purchase.order.line'
    _inherit ='purchase.order.line'
    _columns = {
        'special_sale': fields.boolean('Venta Especial'),
        'ref_customer': fields.char('Referencia Cliente', size=128),
        }