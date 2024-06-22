import base64
import subprocess
import time
import os

class GenerateCSR:
    def __init__(self, working_directory=None):
        """
        Initializes the GenerateCSR class.
        """
        self.csr_type = None
        self.C = None
        self.CN = None
        self.O = None
        self.OU = None
        self.SN = None
        self.UID = None
        self.TITLE = None
        self.CATEGORY = None
        self.ADDRESS = None
        self.working_directory = working_directory or os.path.dirname(os.path.abspath(__file__))

    def run_command(self, command):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result

    def pro_create_key(self):
        os.chdir(self.working_directory)

        commands = [
            ['openssl', 'ecparam', '-name', 'secp256k1', '-genkey', '-noout', '-out', 'PrivateKey.pem'],
            ['openssl', 'ec', '-in', 'PrivateKey.pem', '-pubout', '-conv_form', 'compressed', '-out', 'PublicKey.pem'],
            ['openssl', 'base64', '-d', '-in', 'PublicKey.pem', '-out', 'PublicKey.bin']
        ]

        for command in commands:
            result = self.run_command(command)
            if result.returncode != 0:
                return  # Exit if any command fails

        print("Key generation and conversion successful")

    def create_configuration(self, **data):
        os.chdir(self.working_directory)

        red = "default.cnf"
        wrt = "openssl.cnf"

        with open(red, 'r') as f:
            filedata = f.read()

        replacements = {
            "C=C": "C=" + str(data.get('C', '')),
            "CN=CN": "CN=" + str(data.get('CN', '')),
            "O=O": "O=" + str(data.get('O', '')),
            "OU=OU": "OU=" + str(data.get('OU', '')),
            "SN=SN": "SN=" + str(data.get('SN', '')),
            "UID=UUIDS": "UID=" + str(data.get('UID', '')),
            "title=titles": "title=" + str(data.get('TITLE', '')),
            "registeredAddress=Zatca": "registeredAddress=" + str(data.get('ADDRESS', '')),
            "businessCategory=Zatca": "businessCategory=" + str(data.get('CATEGORY', '')),
            "TYPE=TYPE": str(data.get('TYPE', '')),
        }

        for key, value in replacements.items():
            filedata = filedata.replace(key, value)

        with open(wrt, 'w') as t:
            t.write(filedata)

    def generate_csr(self, csr_type, C, CN, O, OU, SN, UID, TITLE, CATEGORY, ADDRESS):
        os.chdir(self.working_directory)

        if csr_type == "sandbox":
            customoid = b"..TESTZATCA-Code-Signing"
        elif csr_type == "simulation":
            customoid = b"..PREZATCA-Code-Signing"
        else:
            customoid = b"..ZATCA-Code-Signing"

        self.pro_create_key()
        self.create_configuration(
            C=C, CN=CN, O=O, OU=OU, SN=SN, UID=UID, TITLE=TITLE, CATEGORY=CATEGORY, ADDRESS=ADDRESS, TYPE=customoid
        )

        command = [
            "openssl", "req", "-new", "-sha256",
            "-key", "PrivateKey.pem",
            "-extensions", "v3_req",
            "-config", "openssl.cnf",
            "-out", "cert.csr"
        ]

        result = self.run_command(command)
        if result.returncode != 0:
            return {"status": 500, "error": result.stderr}

        # Wait a moment for the file to be written
        time.sleep(0.5)

        try:
            with open("cert.csr", "r") as f, open("PrivateKey.pem", "r") as pvt, open("PublicKey.pem", "r") as pbl:
                basestr = base64.b64encode(f.read().encode('utf-8')).decode('utf-8')
                response = {
                    "status": 200,
                    "certificate_signing_request": basestr,
                    "private_key": pvt.read()[31:-30].replace('\n', ''),
                    "public_key": pbl.read()[27:-25].replace('\n', '')
                }
        except Exception as e:
            response = {"status": 500, "error": str(e)}

        return response
