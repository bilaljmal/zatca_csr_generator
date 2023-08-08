from cryptography import x509
from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.bindings._rust import ObjectIdentifier
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
import base64

class GenerateCSR:
    def __init__(self):

        """
        Initializes the GenerateCSR class.
        """
        self.csr_type = None
        self.C = None
        self.N = None
        self.O = None
        self.OU = None
        self.SN = None
        self.UID = None
        self.TITLE = None
        self.CATEGORY = None
        self.ADDRESS = None

    def generate_key(self):
        private_key = ec.generate_private_key(ec.SECP256K1(), backend=default_backend())
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_key_pem

    def create_custom_extension(self,oid_string, value):
        oid = ObjectIdentifier(oid_string)
        ext = x509.extensions.UnrecognizedExtension(oid, value)
        return ext

    def generate_csr(self, csr_type, C, CN, O, OU, SN, UID, TITLE, CATEGORY, ADDRESS):
        if csr_type == "sandbox":
            customoid = b"..TESTZATCA-Code-Signing"
        elif csr_type == "simulation":
            customoid = b"..PREZATCA-Code-Signing"
        else:
            customoid = b"..ZATCA-Code-Signing"

        private_key_pem = self.generate_key()
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        custom_oid_string = "1.3.6.1.4.1.311.20.2"
        custom_value = customoid
        custom_extension = self.create_custom_extension(custom_oid_string, custom_value)
        dn = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, CN),
            x509.NameAttribute(NameOID.COUNTRY_NAME, C),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, O),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, OU),
        ])
        alt_name = x509.SubjectAlternativeName({
            x509.DirectoryName(x509.Name([
                x509.NameAttribute(NameOID.SURNAME, SN),
                x509.NameAttribute(NameOID.USER_ID, UID),
                x509.NameAttribute(NameOID.TITLE, TITLE),
                x509.NameAttribute(NameOID.BUSINESS_CATEGORY, CATEGORY + "/registeredAddress=" + ADDRESS),
            ])),
        })

        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(dn)
            .add_extension(custom_extension, critical=False)
            .add_extension(alt_name, critical=False)
            .sign(private_key, hashes.SHA256(), backend=default_backend())
        )
        mycsr = csr.public_bytes(serialization.Encoding.PEM)
        base64csr = base64.b64encode(mycsr)
        encoded_string = base64csr.decode('utf-8')
        return private_key_pem,encoded_string
