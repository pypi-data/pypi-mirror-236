Python for CryptoSys PKI
===================================

This is a Python interface to the **CryptoSys PKI Pro** library. 

CryptoSys PKI Pro is a library to carry out public key cryptography using RSA and ECDSA. 
You can generate and manage X.509 certificates, PKCS#8/PKCS#12 private keys and CMS/PKCS#7 objects. 
It includes all required supporting cryptographic utilities. 


CryptoSys PKI Pro v22.0 or above must be installed on your system.
This is available from

    https://www.cryptosys.net/pki/.


To use in Python's REPL
-----------------------


.. code-block:: python

    >>> from cryptosyspki import *
    >>> Gen.version() # "hello world!" for CryptoSys PKI
    210000
    >>> Hash.hex_from_data(b'abc') # compute SHA-1 hash in hex of 'abc' as bytes
    'a9993e364706816aba3e25717850c26c9cd0d89d'
    >>> Hash.hex_from_string('abc', Hash.Alg.SHA256)   # same but over a string and using SHA-256
    'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    >>> h = Hash.data(b'abc')   # h is a byte array (bytes->bytes)
    >>> print(Cnv.tohex(h))     # display the byte array in hex
    A9993E364706816ABA3E25717850C26C9CD0D89D

If you don't like ``import *`` and find ``cryptosyspki`` a bit long to
type each time, try


.. code-block:: python

    >>> import cryptosyspki as pki
    >>> pki.Gen.version() #  Underlying core PKI dll
    210000
    >>> pki.__version__   # cryptosyspki.py package
    '21.0.0'


Examples
--------

There is a series of tests in ``test_pki.py`` (`source <https://cryptosys.net/pki/test_pki.py.html>`_). 
You should find an example there of what you want to do.

These tests require a subdirectory ``work`` in the same folder
which must contain all the required test files.
A spare set of these test files is available separately in ``pkiPythonTestFiles.zip``


::

    test
    |   test_pki.py
    |
    \---work
        |   <...all required test files>
        |
        \---tmp.XXXXXXXX
                <..temporary files...>


The test function creates a new temporary subdirectory each time, which is deleted automatically.
If you want to keep this temp folder for debugging, then add the argument ``nodelete`` on the command line.

This structure is already set up in the distribution file, so unzip the
file ``cryptosyspki-x.x.x.zip`` and open a command-line prompt in the
``test`` subdirectory. You can do any of the following.

1. ``python test_pki.py``

2. ``py.test -v``

3. Open the file ``test_pki.py`` using IDLE and select
   ``Run > Run Module (F5)``.

We've tested this using the Python 3.12.0 interpreter and IDLE, PyCharm 2023.2, and ``py.test``.


Contact
-------

For more information or to make suggestions, please contact us at
https://www.cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd
| Australia
| <https://www.di-mgt.com.au> <https://www.cryptosys.net>
| 19 October 2023
