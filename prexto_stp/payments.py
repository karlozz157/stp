import requests
import os

from bs4 import BeautifulSoup

from .settings import STP
from .utils import Signer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Stp(object):
    def __init__(self, debug=False):
        self.debug = debug

    def pay(self, pay_order):
        """
        Procesa la orden
        """
        request_as_xml = self.__get_request_as_xml(pay_order)

        headers = {
            'Content-Type': 'text/xml; charset="utf-8"',
            'Content-Length': '{}'.format(len(request_as_xml)),
        }

        if self.debug:
            print(request_as_xml)

        response = requests.post(STP['url'], data=request_as_xml, headers=headers)

        return self.__parse_response(str(response.content, 'utf-8'))

    def __get_signature(self, pay_order):
        """
        Firma los datos con el certificado
        """
        return Signer.sign(pay_order.firma)

    def __get_request_as_xml(self, pay_order):
        """
        Llena el xml con los datos del pay order
        """
        xml_template = self.__get_xml_template()

        return xml_template.format(
                pay_order.clave_rastreo,
                pay_order.concepto_pago,
                pay_order.cuenta_beneficiario,
                pay_order.cuenta_ordenante,
                pay_order.email_beneficiario,
                pay_order.empresa,
                self.__get_signature(pay_order),
                pay_order.institucion_contraparte,
                pay_order.institucion_operante,
                pay_order.monto,
                pay_order.nombre_beneficiario,
                pay_order.referencia_numerica,
                pay_order.rfc_curp_beneficiario,
                pay_order.tipo_cuenta_beneficiario,
                pay_order.tipo_pago
            )

    def __get_xml_template(self):
        """
        Obtiene el xml base para construir la petición
        """
        f = open(os.path.join(BASE_DIR, 'template.xml'), 'r')
        xml_template = f.read()
        f.close()

        return xml_template

    def __parse_response(self, response):
        """
        Parsea el xml del response para obtener el id
        """
        xml_soup = BeautifulSoup(response, 'xml')

        if self.debug:
            print(xml_soup)

        return_tag = xml_soup.find('return')

        if return_tag is None:
            raise Exception('houston we have a problem')

        id_tag = return_tag.find('id')
        description_error_tag = return_tag.find('descripcionError')

        if description_error_tag is not None:
            raise Exception('id: {}, error: {}'.format(id_tag.text, description_error_tag.text))

        return id_tag.text
