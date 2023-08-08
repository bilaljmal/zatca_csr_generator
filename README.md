# Csr and Private Key generator for Zatca Phase2
Generate Private Key with EC Curve and CSR for the Zatca Phase2 for the complience CSID
## Installation

To use the Zatca Csr Generator, you need to have cryptography installed. You can install it using pip:

```shell
pip install zatca_csr_generator
```

# Usage
First, import the necessary modules:

Then, import and create an instance of the CsrGenerator class:
```
from zatca_csr_generator import zatca_csr
certificate=GenerateCSR()
```


# Loading an method to obtain private key and certificate signing request
To load an image from a file, use the load_image method:

1. csr_type 
   e.g for 'sandbox' |'simulation' | 'production'. 
2. C = country
    country with max 2 length.
3. CN = common name
4. O = organization
5. OU = organization unit
6. SN = Serial number e.g 
   1-name of the company|2-version|3-uuid
     
7. UID = Tax Registration No (15 Digits)
8. TITLE = Type of business e.g 1000,0100, 1100
   + B2B =0100
   + B2C= 1000
   + Both= 1100
9. CATEGORY = Type of business
10. ADDRESS  = Registered Business Address

```
privatekey,csr= certificate.generate_csr.(csr_type, C, CN, O, OU, SN, UID, TITLE, CATEGORY, ADDRESS)
```
privatekey will return the string for the private key and 

# Example

```
from zatca_csr_generator import zatca_csr

certificate = zatca_csr.GenerateCSR()


privatekey,csr = certificate.generate_csr("production","SA", "TST", "TST",
                                          "TST", "1-TST|2-TEST|3-uuid",
                                          "3210124145101243", "1100", "Information Technology", "RHSX46590")

print(privatekey)
print(csr)
```

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.


# License
This project is open source and licensed under the MIT License.

# Contact

For any questions or inquiries, please contact:

- Muhammad Bilal
- Email: bilaljmal@gmail.com