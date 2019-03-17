import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMPRESA = 'PREXTO'

INSTITUCION_OPERANTE_STP = 90646

TIPO_CUENTA_BENEFICIARIO_CLABE = 40

TIPO_PAGO_TERCERO = 1

STP = {
    'url': 'https://prod.stpmex.com:7002/spei/webservices/SpeiActualizaServices?wsdl',
    'signature': 'RSA-SHA256',
    'pemfile': 'PREXTO-PEM.pem',
    'passphrase': 'Prexto@2019'
}
