# -*- encoding: utf-8 -*-

{
    'name': 'TyP Venta Especial',
    'version': '0.1',
    "author" : "Cmexia",
    "category" : "TyP",
    'description': """
    Este modulo permite capturar la informacion para los pedidos de tipo especial desde las cotizaciones,
    podemos encontrar el reporte desde el modulo de impresion generico de openerp.
    

    """,
    "website" : "www.typrefrigeracion.com.mx",
    "license" : "AGPL-3",
    "depends" : ["sale","purchase"],
    "init_xml" : [],
    "demo_xml" : [],
    "data": [
        "report/special_sale.xml"
        ],
    "update_xml" : [
        "sale_view.xml",
        "purchase_view.xml",
                    ],
    "installable" : True,
    "active" : False,
}
