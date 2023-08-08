from setuptools import setup

setup(
    name='zatca_csr_generator',
    version='0.2.0',
    description='Zatca Csr Generator generates the certificate signing request for zatca phase2, '
                'It is takes informations and parameters from the user and returns the csr in base64 ready to submit to zatca',
    author='Muhammad Bilal',
    author_email='bilaljmal@gmail.com',
    url='https://github.com/bilaljmal/zatca_csr_generator',
    packages=['zatca_csr_generator'],
    install_requires=['cryptography'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)