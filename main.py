from prexto_stp.payments import Stp
from prexto_stp.entities import PayOrder

pay_order = PayOrder()

""" start datos requeridos """
pay_order.monto = 1.00
pay_order.concepto_pago = 'Prueba'
pay_order.institucion_contraparte = '40012' # ver catálogos de instituciones
pay_order.email_beneficiario = 'dandelgadomendoza@gmail.com'
pay_order.nombre_beneficiario = 'Dan Delgado Mendoza'
pay_order.cuenta_beneficiario = '012180026966668258' # cuenta clabe
pay_order.rfc_curp_beneficiario = 'DEMD101013F75'
""" end datos requeridos """

try:
    stp = Stp()
    print(stp.pay(pay_order)) # regresa el id de la transacción
except Exception as e:
    # ver catálogos de los errores
    print('Hubo un error: {}'.format(e.message))
