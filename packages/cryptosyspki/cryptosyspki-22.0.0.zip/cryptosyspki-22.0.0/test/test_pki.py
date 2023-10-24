#! python3
# -*- coding: utf-8 -*-

"""Some tests for ``cryptosyspki`` the Python interface to CryptoSys PKI"""

# test_pki.py: version 22.0.0
# $Date: 2023-10-21 13:31:00 $

# ************************** LICENSE *****************************************
# Copyright (C) 2016-23 David Ireland, DI Management Services Pty Limited.
# All rights reserved. <www.di-mgt.com.au> <www.cryptosys.net>
# The code in this module is licensed under the terms of the MIT license.
# @license MIT
# For a copy, see <http://opensource.org/licenses/MIT>
# ****************************************************************************

from cryptosyspki import *  # @UnusedWildImport
import cryptosyspki as pki  # for pki.__version__
import os
import sys
import pytest
import shutil
from glob import iglob

_MIN_PKI_VERSION = 220000

# Show some info about the core CryptoSys PKI DLL
print("PKI version =", Gen.version())
print("module_name =", Gen.module_name())
print("compile_time =", Gen.compile_time())
print("platform =", Gen.core_platform())
print("licence_type =", Gen.licence_type())
print("module_info =", Gen.module_info())
# Show some system values
print("sys.getdefaultencoding()=", sys.getdefaultencoding())
print("sys.getfilesystemencoding()=", sys.getfilesystemencoding())
print("sys.platform()=", sys.platform)
print("cwd =", os.getcwd())

if Gen.version() < _MIN_PKI_VERSION:
    raise Exception('Require PKI version ' +
                    str(_MIN_PKI_VERSION) + ' or greater')

# GLOBAL VARS
# Remember CWD where we started
start_dir = os.getcwd()
# Temp directory to use as CWD for tests - set by  `setup_temp_dir()`
ourtmp_dir = ""
# Flag to delete tmp directory when finished - used in `reset_start_dir()`
# Change with command-line argument `nodelete` - see `main()`
delete_tmp_dir = True


# JIGGERY-POKERY FOR A TEMP WORKING DIRECTORY
#    start_dir/
#        test_py  # this module
#        work/        # this _must_ exist
#            <all required test files>
#            pki_tmp.XXXXXXXX/    # created by `setup_temp_dir()`
#                <copy of all required test files>
#                <files created by tests>


def setup_temp_dir():
    """Set up a fresh temp directory to work in"""
    global ourtmp_dir
    # `work` should be a sub-directory of the cwd and must exist
    work_dir = os.path.join(start_dir, "work")
    print("\nExpecting to find work dir:", work_dir)
    assert os.path.isdir(work_dir)
    # It should contain all the required test files
    # Create a temp sub-directory in `work`
    ourtmp_dir = os.path.join(work_dir, "pki_tmp." + Cnv.tohex(Rng.bytestring(4)))
    os.mkdir(ourtmp_dir)
    assert (os.path.isdir(ourtmp_dir))
    # copy the required temp files
    for f in iglob(os.path.join(work_dir, "*.*")):
        if (os.path.isfile(f) and not f.endswith('.zip')):
            shutil.copy(f, ourtmp_dir)

    # Set CWD to be inside temp
    os.chdir(ourtmp_dir)
    print("Working in new temp directory:", os.getcwd())


def reset_start_dir():
    if not os.path.isdir(start_dir):
        return
    if (ourtmp_dir == start_dir):
        return
    os.chdir(start_dir)
    print("")
    # print("CWD:", os.getcwd())
    # Remove the temp direcory
    if (delete_tmp_dir and 'pki_tmp' in ourtmp_dir):
        print("Removing temp directory:", ourtmp_dir)
        # time.sleep(2)
        shutil.rmtree(ourtmp_dir, ignore_errors=True)


# MORE JIGGERY_POKERY FOR py.test
@pytest.fixture(scope="module", autouse=True)
def divider_module(request):
    print("\n   --- module %s() start ---" % request.module.__name__)
    setup_temp_dir()

    def fin():
        print("\n   --- module %s() done ---" % request.module.__name__)
        reset_start_dir()

    request.addfinalizer(fin)


@pytest.fixture(scope="function", autouse=True)
def divider_function(request):
    print("\n   --- function %s() start ---" % request.function.__name__)
    os.chdir(ourtmp_dir)

    def fin():
        print("\n   --- function %s() done ---" % request.function.__name__)
        os.chdir(start_dir)

    request.addfinalizer(fin)


# FILE-RELATED UTILITIES
def read_binary_file(fname):
    with open(fname, "rb") as f:
        return bytearray(f.read())


def write_binary_file(fname, data):
    with open(fname, "wb") as f:
        f.write(data)


def read_text_file(fname, enc='utf8'):
    with open(fname, encoding=enc) as f:
        return f.read()


def write_text_file(fname, s, enc='utf8'):
    with open(fname, "w", encoding=enc) as f:
        f.write(s)


def _print_file(fname):
    """Print contents of text file."""
    s = read_text_file(fname)
    print(s)


def _print_file_hex(fname):
    """Print contents of file encoded in hexadecimal."""
    b = read_binary_file(fname)
    print(Cnv.tohex(b))


def _dump_file(fname):
    """Print contents of text file with filename header and rulers."""
    s = read_text_file(fname)
    ndash = (24 if len(s) > 24 else len(s))
    print("FILE:", fname)
    print("-" * ndash)
    print(s)
    print("-" * ndash)


def _dump_and_print_asn1(fname, opts=0):
    print("FILE:", fname)
    try:
        s = Asn1.text_dump_tostring(fname, opts)
        print(s)
    except PKIError as e:
        print("Woops! PKIError:", e)


def _dump_and_print_x509(fname, opts=0):
    try:
        s = X509.text_dump_tostring(fname, opts)
        print(s)
    except PKIError as e:
        print("Woops! PKIError:", e)


#############
# THE TESTS #
#############


def test_version():
    assert Gen.version() >= _MIN_PKI_VERSION


def test_error_lookup():
    print("\nLOOKUP SOME ERROR CODES...")
    for n in range(10):
        s = Gen.error_lookup(n)
        print("error_lookup(" + str(n) + ")=" + s)
        assert (len(s) > 0)


def test_cnv():
    print("\nTEST CNV FUNCTIONS...")

    # hex --> bytes --> base64
    b = Cnv.fromhex("FE DC BA 98 76 54 32 10")
    print("b=0x" + Cnv.tohex(b))
    print("b64(b)=" + Cnv.tobase64(b))
    assert (Cnv.tobase64(b) == "/ty6mHZUMhA=")

    # base64 --> bytes --> hex --> base64
    b = Cnv.frombase64("/ty6mHZUMhA=")
    print("b=0x" + Cnv.tohex(b))
    assert (Cnv.tohex(b) == "FEDCBA9876543210")
    print("b64(b)=" + Cnv.tobase64(b))
    assert (Cnv.tobase64(b) == "/ty6mHZUMhA=")

    # hex --> bytes --> base58
    b = Cnv.fromhex("00010966776006953D5567439E5E39F86A0D273BEED61967F6")
    print("b=0x" + Cnv.tohex(b))
    print("b58(b)=" + Cnv.tobase58(b))
    assert (Cnv.tobase58(b) == "16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM")

    # base58 --> bytes --> hex
    h = Cnv.tohex(Cnv.frombase58("16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM"))
    print(h)
    assert (h == "00010966776006953D5567439E5E39F86A0D273BEED61967F6")

    # reverse bytes
    print("Using Cnv.reverse_bytes()...")
    b = Cnv.fromhex("DEADBEEF01")
    print("INPUT: ", Cnv.tohex(b))
    r = Cnv.reverse_bytes(b)
    print("OUTPUT:", Cnv.tohex(r))
    assert (Cnv.tohex(r) == "01EFBEADDE")

    # Possible corner cases...
    print("Test empty string...")
    b = Cnv.fromhex("")
    print("INPUT: ", Cnv.tohex(b))
    r = Cnv.reverse_bytes(b)
    print("OUTPUT:", Cnv.tohex(r))
    assert (Cnv.tohex(r) == "")

    b = Cnv.fromhex("01")
    print("INPUT: ", Cnv.tohex(b))
    r = Cnv.reverse_bytes(b)
    print("OUTPUT:", Cnv.tohex(r))
    assert (Cnv.tohex(r) == "01")

    b = Cnv.fromhex("0102")
    print("INPUT: ", Cnv.tohex(b))
    r = Cnv.reverse_bytes(b)
    print("OUTPUT:", Cnv.tohex(r))
    assert (Cnv.tohex(r) == "0201")

    print("Using Cnv.num_from_bytes()...")
    b = Cnv.fromhex("DEADBEEF")
    print("INPUT:", Cnv.tohex(b))
    # Default big-endian order
    n = Cnv.num_from_bytes(b)
    print("BE:", hex(n))
    assert (0xdeadbeef == n)
    # Little-endian order
    n = Cnv.num_from_bytes(b, endn=Cnv.EndianNess.LITTLE_ENDIAN)
    print("LE:", hex(n))
    assert (0xEFBEADDE == n)

    # Input shorter than 4 bytes is padded on the right with zeros
    b = b[:3]
    print("INPUT:", Cnv.tohex(b))
    n = Cnv.num_from_bytes(b)
    print("BE:", hex(n))
    assert (0xDEADBE00 == n)
    n = Cnv.num_from_bytes(b, endn=Cnv.EndianNess.LITTLE_ENDIAN)
    print("LE:", hex(n))
    assert (0xBEADDE == n)

    print("Using Cnv.num_to_bytes()...")
    n = 0xDEADBEEF
    b = Cnv.num_to_bytes(n)
    print("BE:", Cnv.tohex(b))
    b = Cnv.num_to_bytes(n, endn=Cnv.EndianNess.LITTLE_ENDIAN)
    print("LE:", Cnv.tohex(b))

    n = 0x01
    b = Cnv.num_to_bytes(n)
    print("BE:", Cnv.tohex(b))
    b = Cnv.num_to_bytes(n, endn=Cnv.EndianNess.LITTLE_ENDIAN)
    print("LE:", Cnv.tohex(b))


def test_cnv_utf8():
    print("\nTEST CNV UTF-8 CHECKS...")

    print("Bytes representing simple ASCII characters")
    s = b'abc'
    print("s=0x" + Cnv.tohex(s))
    n = Cnv.utf8_check(s)
    print("Cnv.utf8_check(s)=", n, "(expecting 1)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (1 == n)

    # A string containing a Latin-1 character, LATIN SMALL LETTER E WITH ACUTE
    # -- this is invalid UTF-8
    print("Bytes representing a string containing a Latin-1 character")
    s = b"M\xe9xico"
    print("s=0x" + Cnv.tohex(s))
    n = Cnv.utf8_check(s)
    print("Cnv.utf8_check(s)=", n, "(expecting 0)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (0 == n)

    # A byte array with a valid UTF-8-encoded array of chinese characters:
    # zhong guo (U+4E2D, U+56FD)
    b = Cnv.fromhex('e4b8ade59bbd')
    print("Chinese characters: zhong guo (U+4E2D, U+56FD) encoded in UTF-8")
    print("b=0x" + Cnv.tohex(b))
    n = Cnv.utf8_check(b)
    print("Cnv.utf8_check(b)=", n, "(expecting 3)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (3 == n)

    # lookup invalid code
    print("Cnv.utf8_check_to_string(42)=>", Cnv.utf8_check_to_string(42))

    print("Bad UTF-8 (chopped)")
    b = b"\xc3\xb3\xc3\xa9\xc3\xad\xc3\xa1\xc3"
    print("b=0x" + Cnv.tohex(b))
    n = Cnv.utf8_check(b)
    print("Cnv.utf8_check(b)=", n, "(expecting 0)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (0 == n)

    print("Bad UTF-8 (illegal)")
    b = b"\xef\xbf\xbf"
    print("b=0x" + Cnv.tohex(b))
    n = Cnv.utf8_check(b)
    print("Cnv.utf8_check(b)=", n, "(expecting 0)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (0 == n)

    print("Check some files...")
    fname = 'test-iso88591.xml'
    n = Cnv.utf8_check_file(fname)
    print("Cnv.utf8_check_file('" + fname + "')=", n, "(expecting 0)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (0 == n)
    fname = 'test-utf8.xml'
    n = Cnv.utf8_check_file(fname)
    print("Cnv.utf8_check_file('" + fname + "')=", n, "(expecting 2)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (2 == n)
    fname = 'test-daiwei.xml'
    n = Cnv.utf8_check_file(fname)
    print("Cnv.utf8_check_file('" + fname + "')=", n, "(expecting 3)")
    print(n, '==>', Cnv.utf8_check_to_string(n))
    assert (3 == n)


def test_cipher():
    print("\nTEST BLOCK CIPHER FUNCTIONS...")

    algstr = "Tdea/CBC/PKCS5"
    print(algstr)
    key = bytearray.fromhex('737C791F25EAD0E04629254352F7DC6291E5CB26917ADA32')
    iv = bytearray.fromhex("B36B6BFB6231084E")
    pt = bytearray.fromhex("5468697320736F6D652073616D706520636F6E74656E742E")

    ct = Cipher.encrypt(pt, key, iv, algstr)
    print(Cnv.tohex(ct))
    b = bytearray.fromhex("5468697320736F6D652073616D706520636F6E74656E742E")
    print(b)
    assert (ct == bytearray.fromhex(
        "D76FD1178FBD02F84231F5C1D2A2F74A4159482964F675248254223DAF9AF8E4"))
    p1 = Cipher.decrypt(ct, key, iv, algstr)
    print(p1)
    assert (p1 == pt)

    print("Use default ECB mode (IV is ignored)")
    ct = Cipher.encrypt(pt, key, alg=Cipher.Alg.TDEA)
    print(Cnv.tohex(ct))
    p1 = Cipher.decrypt(ct, key, alg=Cipher.Alg.TDEA)
    print(p1)
    assert (p1 == pt)

    ct = Cipher.encrypt(pt, key, iv, mode=Cipher.Mode.CBC,
                        alg=Cipher.Alg.TDEA)
    print(Cnv.tohex(ct))
    p1 = Cipher.decrypt(ct, key, iv, mode=Cipher.Mode.CBC,
                        alg=Cipher.Alg.TDEA)
    print(p1)
    assert (p1 == pt)

    algstr = "Aes128/CBC/pkcs5"
    print(algstr)
    key = bytearray.fromhex('0123456789ABCDEFF0E1D2C3B4A59687')
    iv = bytearray.fromhex("FEDCBA9876543210FEDCBA9876543210")
    # In Python 3 we must must pass plaintext as bytes; ASCII strings no longer work
    pt = b"Now is the time for all good men to"
    ct = Cipher.encrypt(pt, key, iv, algstr)
    print(Cnv.tohex(ct))
    assert (ct == bytearray.fromhex(
        "C3153108A8DD340C0BCB1DFE8D25D2320EE0E66BD2BB4A313FB75C5638E9E17753C7E8DF5975A36677355F5C6584228B"))
    # Now decrypt using flags instead of alg string
    p1 = Cipher.decrypt(ct, key, iv, alg=Cipher.Alg.AES128,
                        mode=Cipher.Mode.CBC, pad=Cipher.Pad.PKCS5)
    print("P':", p1)
    assert (p1 == pt)

    algstr = "Aes128/ECB/OneAndZeroes"
    print(algstr)
    ct = Cipher.encrypt(pt, key, algmodepad=algstr)
    print("CT:", Cnv.tohex(ct))
    p1 = Cipher.decrypt(ct, key, algmodepad="Aes128/ECB/NoPad")
    print("Pn:", Cnv.tohex(p1))
    p1 = Cipher.decrypt(ct, key, algmodepad=algstr)
    print("P':", Cnv.tohex(p1))
    print("P':", p1)
    assert (p1 == pt)


def test_cipher_hex():
    print("\nTEST CIPHER FUNCTIONS USING HEX-ENCODED PARAMETERS...")
    algstr = "Tdea/CBC/PKCS5"
    print("ALG:", algstr)
    keyhex = '737C791F25EAD0E04629254352F7DC6291E5CB26917ADA32'
    ivhex = "B36B6BFB6231084E"
    pthex = "5468697320736F6D652073616D706520636F6E74656E742E"
    okhex = "D76FD1178FBD02F84231F5C1D2A2F74A4159482964F675248254223DAF9AF8E4"
    print("KY:", keyhex)
    print("IV:", ivhex)
    print("PT:", pthex)
    cthex = Cipher.encrypt_hex(pthex, keyhex, ivhex, algstr)
    print("CT:", cthex)
    print("OK:", okhex)
    assert cthex == okhex, "Cipher.encrypt_hex failed"
    print("About to decrypt...")
    # Decrypt using flags instead of alg string
    p1hex = Cipher.decrypt_hex(cthex, keyhex, ivhex, alg=Cipher.Alg.TDEA, mode=Cipher.Mode.CBC, pad=Cipher.Pad.PKCS5)
    print("P':", p1hex)
    assert p1hex == pthex

    # Another example, this time with the IV prefixed to the ciphertext
    algstr = "Aes128/CBC/OneAndZeroes"
    keyhex = '0123456789ABCDEFF0E1D2C3B4A59687'
    ivhex = "FEDCBA9876543210FEDCBA9876543210"
    pthex = "4E6F77206973207468652074696D6520666F7220616C6C20676F6F64206D656E20746F"
    # IV||CT
    okhex = "FEDCBA9876543210FEDCBA9876543210C3153108A8DD340C0BCB1DFE8D25D2320EE0E66BD2BB4A313FB75C5638E9E1771D4CDA34FBFB7E74B321F9A2CF4EA61B"
    print("KY:", keyhex)
    print("IV:", ivhex)
    print("PT:", pthex)
    cthex = Cipher.encrypt_hex(pthex, keyhex, ivhex, algstr, opts=Cipher.Opts.PREFIXIV)
    print("CT:", cthex)
    print("OK:", okhex)
    assert cthex == okhex, "Cipher.encrypt_hex failed"
    # Decrypt using flags instead of alg string - this time we don't need the IV argument
    p1hex = Cipher.decrypt_hex(cthex, keyhex, None, alg=Cipher.Alg.AES128, mode=Cipher.Mode.CBC,
                               pad=Cipher.Pad.ONEANDZEROES, opts=Cipher.Opts.PREFIXIV)
    print("P':", p1hex)
    assert (p1hex == pthex)


def test_cipher_block():
    print("\nTEST CIPHER FUNCTIONS WITH EXACT BLOCK LENGTHS...")
    key = Cnv.fromhex("0123456789ABCDEFF0E1D2C3B4A59687")
    iv = Cnv.fromhex("FEDCBA9876543210FEDCBA9876543210")
    print("KY:", Cnv.tohex(key))
    print("IV:", Cnv.tohex(iv))
    # In Python 3 plaintext must be bytes, not ASCII string
    pt = b"Now is the time for all good men"
    print("PT:", pt)
    print("PT:", Cnv.tohex(pt))
    okhex = "C3153108A8DD340C0BCB1DFE8D25D2320EE0E66BD2BB4A313FB75C5638E9E177"
    ct = Cipher.encrypt_block(
        pt, key, iv, alg=Cipher.Alg.AES128, mode=Cipher.Mode.CBC)
    print("CT:", Cnv.tohex(ct))
    print("OK:", okhex)
    assert (okhex.upper() == Cnv.tohex(ct))
    p1 = Cipher.decrypt_block(
        ct, key, iv, alg=Cipher.Alg.AES128, mode=Cipher.Mode.CBC)
    print("P1:", Cnv.tohex(p1))
    print("P1:", p1)

    # Using defaults (TDEA/ECB)
    key = Rng.bytestring(Cipher.keybytes(Cipher.Alg.TDEA))
    print("KY:", Cnv.tohex(key))
    ct = Cipher.encrypt_block(pt, key, iv)
    print("CT:", Cnv.tohex(ct))
    p1 = Cipher.decrypt_block(ct, key, iv)
    print("P1:", Cnv.tohex(p1))
    print("P1:", p1)


def test_cipher_file():
    print("\nTEST CIPHER FILE FUNCTIONS...")
    file_pt = "hello.txt"
    write_text_file(file_pt, "hello world\r\n")
    print(file_pt + ":", )
    _print_file_hex(file_pt)
    key = Cnv.fromhex("fedcba9876543210fedcba9876543210")
    iv = Rng.bytestring(Cipher.blockbytes(Cipher.Alg.AES128))
    print("IV:", Cnv.tohex(iv))
    file_ct = "hello.aes128.enc.dat"
    n = Cipher.file_encrypt(file_ct, file_pt, key, iv, "aes128-ctr", opts=Cipher.Opts.PREFIXIV)
    assert (n == 0)
    print(file_ct + ":", )
    _print_file_hex(file_ct)

    file_chk = "hello.aes128.chk.txt"
    n = Cipher.file_decrypt(file_chk, file_ct, key, iv, "aes128-ctr", opts=Cipher.Opts.PREFIXIV)
    assert (n == 0)
    print(file_chk + ":", )
    _print_file_hex(file_chk)
    # check files are equal
    assert (read_binary_file(file_pt) == read_binary_file(file_chk))


def test_cipher_gcm():
    print("\nTEST CIPHER GCM...")
    file_pt = "hello.txt"
    write_text_file(file_pt, "hello world\r\n")
    print(file_pt + ":", )
    _print_file_hex(file_pt)
    key = Cnv.fromhex("fedcba9876543210fedcba9876543210")
    print("KY:", Cnv.tohex(key))
    # NB Require exact 12-byte IV for GCM
    iv = Cnv.fromhex("000102030405060708090A0B")
    print("IV:", Cnv.tohex(iv))
    file_ct = "hello.aes128.gcm.enc.dat"
    n = Cipher.file_encrypt(file_ct, file_pt, key, iv, "aes128-gcm", opts=Cipher.Opts.PREFIXIV)
    assert (n == 0)
    print(file_ct + ":", )
    _print_file_hex(file_ct)

    file_chk = "hello.aes128.gcm.chk.txt"
    n = Cipher.file_decrypt(file_chk, file_ct, key, iv, "aes128-gcm", opts=Cipher.Opts.PREFIXIV)
    assert (n == 0)
    print(file_chk + ":", )
    _print_file_hex(file_chk)
    # check files are equal
    assert (read_binary_file(file_pt) == read_binary_file(file_chk))

    print("Encrypt using AES-GCM with hex-encoded parameters...")
    # Same as EncryptAEAD except without AAD and with hex-encoded arguments
    keyhex = "2B7E151628AED2A6ABF7158809CF4F3C"
    ivhex = "000102030405060708090A0B"
    pthex = Cnv.tohex("This is some sample content.".encode())
    print("PT =", pthex)
    cthex = Cipher.encrypt_hex(pthex, keyhex, ivhex, "aes128-gcm")
    print("CT =", cthex)
    # CT = 0FA752259801FD6293B779E382FAD5FA7B5664D62EB63AA66064E189024C709ED4D580FB5E04E001C2D8DF97
    assert len(cthex) > 0
    dthex = Cipher.decrypt_hex(cthex, keyhex, ivhex, "aes128-gcm")
    print("DT =", dthex)
    assert len(dthex) > 0, "Cipher.decrypt failed"
    print("DT =", Cnv.fromhex(dthex).decode())
    # Check decrypted hex is equal to original
    assert dthex.upper() == pthex.upper()


def test_cipher_keywrap():
    print("\nTEST CIPHER KEY WRAP FUNCTIONS...")
    # AES-128
    keydata = Cnv.fromhex("00112233 44556677 8899aabb ccddeeff")
    kek = Cnv.fromhex("c17a44e8 e28d7d64 81d1ddd5 0a3b8914")
    wk = Cipher.key_wrap(keydata, kek, Cipher.Alg.AES128)
    print("WK=", Cnv.tohex(wk))
    assert (Cnv.tohex(wk) == "503D75C73630A7B02ECF51B9B29B907749310B77B0B2E054")

    # Unwrap
    k = Cipher.key_unwrap(wk, kek, Cipher.Alg.AES128)
    print("UNWRAPPED K=", Cnv.tohex(k))
    assert (k == keydata)

    # AES-256
    keydata = Cnv.fromhex(
        "8cbedec4 8d063e1b a46be8e3 69a9c398 d8e30ee5 42bc347c 4f30e928 ddd7db49")
    kek = Cnv.fromhex(
        "9e84ee99 e6a84b50 c76cd414 a2d2ec05 8af41bfe 4bf3715b f894c8da 1cd445f6")
    wk = Cipher.key_wrap(keydata, kek, Cipher.Alg.AES256)
    print("WK=", Cnv.tohex(wk))
    assert (Cnv.tohex(
        wk) == "EAFB901F82B98D37F17497063DE3E5EC7246AB57200AE73EDDDDF24AA403DAFA0C5AE151D1746FA4")

    # Unwrap
    k = Cipher.key_unwrap(wk, kek, Cipher.Alg.AES256)
    print("UNWRAPPED K=", Cnv.tohex(k))
    assert (k == keydata)

    # Triple DES
    print("Using Triple DES the result is always different, but will be 16 bytes longer...")
    keydata = Cnv.fromhex(
        "84e7f2d8 78f89fcc cd2d5eba fc56daf7 3300f27e f771cd68")
    kek = Cnv.fromhex("8ad8274e 56f46773 8edd83d4 394e5e29 af7c4089 e4f8d9f4")
    wk = Cipher.key_wrap(keydata, kek, Cipher.Alg.TDEA)
    print("WK=", Cnv.tohex(wk))
    assert len(wk) == len(keydata) + 16

    # Unwrap
    k = Cipher.key_unwrap(wk, kek, Cipher.Alg.TDEA)
    print("UNWRAPPED K=", Cnv.tohex(k))
    assert (k == keydata)


def test_cipher_pad():
    print("\nTEST CIPHER PAD....")

    data = Cnv.fromhex('FFFFFFFFFF')
    print("Input data :", Cnv.tohex(data))
    padded = Cipher.pad(data, Cipher.Alg.TDEA)
    print("Padded data:", Cnv.tohex(padded))
    unpadded = Cipher.unpad(padded, Cipher.Alg.TDEA)
    print("Unpadded   :", Cnv.tohex(unpadded))
    padded = Cipher.pad(data, Cipher.Alg.TDEA,
                        Cipher.Pad.ONEANDZEROES)
    print("Padded data:", Cnv.tohex(padded))
    unpadded = Cipher.unpad(padded, Cipher.Alg.TDEA,
                            Cipher.Pad.ONEANDZEROES)
    print("Unpadded   :", Cnv.tohex(unpadded))

    # Pad the empty string
    data = Cnv.fromhex('')
    print("Input data :", Cnv.tohex(data))
    padded = Cipher.pad(data, Cipher.Alg.AES128)
    print("Padded data:", Cnv.tohex(padded))
    unpadded = Cipher.unpad(padded, Cipher.Alg.AES128)
    print("Unpadded   :", Cnv.tohex(unpadded))
    # Pass data as hex strings
    datahex = 'aaaaaa'
    print("Input data :", datahex)
    paddedhex = Cipher.pad_hex(datahex, Cipher.Alg.TDEA)
    print("Padded data:", paddedhex)
    unpaddedhex = Cipher.unpad_hex(paddedhex, Cipher.Alg.TDEA)
    print("Unpadded   :", unpaddedhex)
    paddedhex = Cipher.pad_hex(
        datahex, Cipher.Alg.TDEA, Cipher.Pad.ONEANDZEROES)
    print("Padded data:", paddedhex)
    unpaddedhex = Cipher.unpad_hex(
        paddedhex, Cipher.Alg.TDEA, Cipher.Pad.ONEANDZEROES)
    print("Unpadded   :", unpaddedhex)


def test_rsa_makekeys():
    print("\nTEST RSA KEY FUNCTIONS....")
    print("Making a new 512-bit RSA key pair...")
    rsaprikeyfile = "myrsaprivate.p8"
    rsapubkeyfile = "myrsapublic.p1"
    # We use 512 bits here for speed. In practice 512 bits is insecure. Use at
    # least 1024
    r = Rsa.make_keys(rsapubkeyfile, rsaprikeyfile, 512,
                      Rsa.PublicExponent.RSAEXP_EQ_65537, 'password')
    assert (0 == r)

    # Read from new key file into an "internal" key string
    prikeystr = Rsa.read_private_key(rsaprikeyfile, 'password')
    # Internal key string should be treated as a "blob".
    print("prikeystr =", prikeystr)
    assert (len(prikeystr) > 0)
    nbits = Rsa.key_bits(prikeystr)
    print("nbits = ", nbits)
    assert (nbits > 0)
    print("hashcode =", Rsa.key_hashcode(prikeystr))

    pubkeystr = Rsa.read_public_key(rsapubkeyfile)
    print("pubkeystr =", pubkeystr)
    assert (len(pubkeystr) > 0)
    nbits = Rsa.key_bits(pubkeystr)
    print("nbits = ", nbits)
    assert (nbits > 0)
    print("hashcode =", Rsa.key_hashcode(pubkeystr))

    s = Rsa.key_value(pubkeystr, "Exponent")
    print("exponent in base64:", s)
    s = Rsa.key_value(pubkeystr, "MODULUS")
    print("modulus in base64:", s)

    # Create an XML representation of the internal string - force values in
    # non-standard hex
    s = Rsa.to_xmlstring(pubkeystr, Rsa.XmlOptions.HEXBINARY)
    print("xml (hex):", s)

    # Again using standard default base64 values
    s = Rsa.to_xmlstring(pubkeystr)
    print("xml:", s)

    # Go back from XML string to a new internal string (this will not be the
    # same as before)
    s = Rsa.from_xmlstring(s)
    print("new keystr:", s)
    # But should have the same key hashcode
    print("hashcode =", Rsa.key_hashcode(s))


def test_rsa_errors():
    print("\nTry to use an invalid keystr...")
    try:
        Rsa.key_hashcode('')
    except PKIError as e:
        print("(Expected) PKIError:", e)


def test_rsa_savekeys():
    print("\nTEST READING RSA KEYS THEN RE-SAVING IN DIFFERENT FORMAT....")
    # Read in a private key
    fname = "AlicePrivRSASign.p8e"
    print("FILE:", fname)
    prikeystr = Rsa.read_private_key(fname, "password")
    print("KeyBits:", Rsa.key_bits(prikeystr))
    print("KeyIsPrivate:", Rsa.key_isprivate(prikeystr))
    print("KeyHashCode:", Rsa.key_hashcode(prikeystr))

    print("Save with stronger encryption...")
    fname = "alice-stronger.p8e"
    Rsa.save_enc_key(fname, prikeystr, "password123",  # Note stronger password here :-)
                     pbescheme=Rsa.PbeScheme.PBKDF2_AES128, params="count=5999", fileformat=Rsa.Format.PEM)
    # Note change [v22.0] here. Formerly it would have been
    # pbescheme=Rsa.PbeScheme.PBKDF2_AES128, count=5999, fileformat=Rsa.Format.PEM)

    _dump_and_print_asn1(fname)
    print("FILE:", fname, "-->", Asn1.type(fname))
    # Check we can read and that key is the same
    keystrchk = Rsa.read_private_key(fname, "password123")
    print("KeyHashCode:", Rsa.key_hashcode(keystrchk))
    assert (Rsa.key_hashcode(keystrchk) == Rsa.key_hashcode(prikeystr))

    print("Save without encryption...")
    fname = "alice-noencrypt.p8"
    Rsa.save_key(fname, prikeystr)
    print("FILE:", fname, "-->", Asn1.type(fname))
    # Check we can read and that key is the same
    keystrchk = Rsa.read_private_key(fname)
    print("KeyHashCode:", Rsa.key_hashcode(keystrchk))
    assert (Rsa.key_hashcode(keystrchk) == Rsa.key_hashcode(prikeystr))

    print("Convert private key string to a public key...")
    pubkeystr = Rsa.publickey_from_private(prikeystr)
    print("KeyBits:", Rsa.key_bits(pubkeystr))
    print("KeyIsPrivate:", Rsa.key_isprivate(pubkeystr))
    print("KeyHashCode:", Rsa.key_hashcode(pubkeystr))

    print("Check the public and private key strings are matched...")
    ismatch = Rsa.key_match(prikeystr, pubkeystr)
    print("Rsa.key_match() returns", ismatch)
    assert (ismatch)

    print("Save to a new file in Open-SSL format...")
    fname = "alice-ssl.pub"
    Rsa.save_key(fname, pubkeystr, fileformat=Rsa.Format.SSL)
    print("FILE:", fname, "-->", Asn1.type(fname))
    # Check we can read and that key is the same
    keystrchk = Rsa.read_public_key(fname)
    print("KeyHashCode:", Rsa.key_hashcode(keystrchk))
    assert (Rsa.key_hashcode(keystrchk) == Rsa.key_hashcode(pubkeystr))


def test_rsa_sign():
    print("\nTEST RSA SIGN....")
    print("Sign in two parts: encode then do raw RSA with private key...")
    # See also Sig.sign() for a cleaner way

    # Read in a private key
    prikeystr = Rsa.read_private_key("AlicePrivRSASign.p8e", "password")
    print(prikeystr)
    message = b'abc'
    # We need the length of the RSA key modulus in bytes
    keybytes = Rsa.key_bytes(prikeystr)
    print("KEYBYTES =", keybytes)
    # 1. Encode the message in a block of the correct size
    #    -- this computes the message digest value automatically
    b = Rsa.encode_msg_for_signature(keybytes, message)
    print("BLK=[" + Cnv.tohex(b) + "]")
    # 2. Encrypt the block using "raw" RSA transform
    sig = Rsa.raw_private(b, prikeystr)
    print("SIG=[" + Cnv.tohex(sig) + "]")

    # To verify the signature we read in the public key
    pubkeystr = Rsa.read_public_key("AliceRSASignByCarl.cer")
    print(pubkeystr)
    # 1. Decrypt the signature to a block using "raw" RSA transform
    blk = Rsa.raw_public(sig, pubkeystr)
    print("BLK=[" + Cnv.tohex(blk) + "]")

    # 2a. Decode to extract the full digestinfo
    #     -- normally we don't do this, but we test it here
    dig = Rsa.decode_digest_for_signature(blk, True)
    print("DIGINFO=[" + Cnv.tohex(dig) + "]")

    # 2b. Decode to extract the digest
    dig = Rsa.decode_digest_for_signature(blk)
    print("DIG=[" + Cnv.tohex(dig) + "]")

    # Check we got a match
    digvalue = Hash.data(b'abc')
    print("SHA1('abc')=", Cnv.tohex(digvalue))
    assert (dig == digvalue)

    print("Do again but start with digest value, and use SHA-256...")
    digvalue = Hash.data(b'abc', Hash.Alg.SHA256)
    print("SHA256('abc')=", Cnv.tohex(digvalue))
    b = Rsa.encode_msg_for_signature(
        keybytes, digvalue, hashalg=Hash.Alg.SHA256, digest_only=True)
    print("BLK=[" + Cnv.tohex(b) + "]")
    sig = Rsa.raw_private(b, prikeystr)
    print("SIG=[" + Cnv.tohex(sig) + "]")
    print("BLK=[" + Cnv.tohex(b) + "]")
    # decode to extract the digest
    dig = Rsa.decode_digest_for_signature(b)
    print("DIG=[" + Cnv.tohex(dig) + "]")


def test_rsa_encrypt():
    print("\nTEST RSA ENCRYPT....")
    print("Encrypt in two parts: encode then do raw RSA with public key...")

    message = b'Hi Bob.'  # Note usually we use RSA to encrypt a session key.
    print("MSG:", message)
    # Read in Bob's public key
    pubkeystr = Rsa.read_public_key("BobRSASignByCarl.cer")
    print(pubkeystr)

    # We need the length of the RSA key modulus in bytes
    keybytes = Rsa.key_bytes(pubkeystr)
    print("KEYBYTES =", keybytes)
    blk = Rsa.encode_msg_for_encryption(keybytes, message)
    print("BLK=[" + Cnv.tohex(blk) + "]")

    ct = Rsa.raw_public(blk, pubkeystr)
    print("Note that the ciphertext block will be different each time...")
    print("CT =[" + Cnv.tohex(ct) + "]")

    print("Decrypt in two parts: do raw RSA with private key then decode...")
    # Read in a private key
    prikeystr = Rsa.read_private_key("BobPrivRSAEncrypt.p8e", "password")
    print(prikeystr)
    blk = Rsa.raw_private(ct, prikeystr)
    print("BLK=[" + Cnv.tohex(blk) + "]")
    pt = Rsa.decode_msg_for_encryption(blk)
    print("PT =[" + Cnv.tohex(ct) + "]")
    # in this case we expect plain ASCII text
    print("PT='" + str(pt) + "'")
    assert (pt == message)

    print("Again using one-step encrypt() and decrypt() this time with OEAP method...")
    # Use key strings we read in above
    print("MSG:", message)
    ct = Rsa.encrypt(message, pubkeystr, method=Rsa.EME.OAEP)
    print("CT =[" + Cnv.tohex(ct) + "]")
    pt = Rsa.decrypt(ct, prikeystr, method=Rsa.EME.OAEP)
    print("PT='" + str(pt) + "'")
    assert (pt == message)

    print("")
    print("RSAES-OAEP Encryption Example 1.1 from `oaep-vect.txt` in `pkcs-1v2-1-vec.zip`")
    print("Encrypt using RSA-OAEP but set seed to be a fixed value to compare with test vector")
    # Use key files directly: RSA key file 1024-bit
    pubkeyfile = "rsa-oaep-1.pub"
    prikeyfile = "rsa-oaep-1.p8"  # unencrypted, no password
    # Message to be encrypted
    msg = Cnv.fromhex("6628194e12073db03ba94cda9ef9532397d50dba79b987004afefe34")
    print("MSG:", Cnv.tohex(msg))
    ct = Rsa.encrypt(msg, pubkeyfile, method=Rsa.EME.OAEP, params="seed=18b776ea21069d69776a33e96bad48e1dda0a5ef")
    print("CT = " + Cnv.tohex(ct))
    # Known answer from test vector
    okhex = "354fe67b4a126d5d35fe36c777791a3f7ba13def484e2d3908aff722fad468fb21696de95d0be911c2d3174f8afcc201035f7b6d8e69402de5451618c21a535fa9d7bfc5b8dd9fc243f8cf927db31322d6e881eaa91a996170e657a05a266426d98c88003f8477c1227094a0d9fa1e8c4024309ce1ecccb5210035d47ac72e8a"
    print("OK = " + okhex)
    assert (Cnv.tohex(ct).lower() == okhex.lower())
    # Decrypt - the private key is unencrypted with no password
    pt = Rsa.decrypt(ct, prikeyfile, "", method=Rsa.EME.OAEP)
    print("PT = " + Cnv.tohex(pt))
    assert (Cnv.tohex(pt).lower() == Cnv.tohex(msg).lower())

    print("Encrypt using RSA-OAEP using SHA-256 for encoding hash function and SHA-1 for MGF hash function...")
    # The result will be different each time
    ct = Rsa.encrypt(msg, pubkeyfile, method=Rsa.EME.OAEP, hashalg=Rsa.HashAlg.SHA256, advopts=Rsa.AdvOpts.MGF1_SHA1)
    print("CT = " + Cnv.tohex(ct))
    # Decrypt - we must specify the parameters used to encrypt
    pt = Rsa.decrypt(ct, prikeyfile, "", method=Rsa.EME.OAEP, hashalg=Rsa.HashAlg.SHA256, advopts=Rsa.AdvOpts.MGF1_SHA1)
    print("PT = " + Cnv.tohex(pt))
    assert (Cnv.tohex(pt).lower() == Cnv.tohex(msg).lower())


def test_x509_generate():
    print("\nTEST X509 FUNCTIONS....")
    # For convenience we hardcode the password - DON'T DO THIS IN PRACTICE!
    mypassword = 'password'
    print("Make a self-signed X.509 certificate:")

    # Generate a new RSA key pair for the CA
    # (in practice, do this once)
    print("Generating a new RSA keypair for the CA...")
    ca_prikeyfile = 'thecaprikey.p8'
    ca_pubkeyfile = 'thecapubkey.p1'
    n = Rsa.make_keys(ca_pubkeyfile, ca_prikeyfile, 1024,
                      Rsa.PublicExponent.RSAEXP_EQ_65537, mypassword)
    assert (0 == n)
    assert (os.path.isfile(ca_prikeyfile))
    assert (os.path.isfile(ca_pubkeyfile))

    # Now use these to create a self-signed X.509 certificate (we only need
    # the private key file)
    ca_certfile = 'theca.cer'
    n = X509.make_cert_self(ca_certfile, ca_prikeyfile,
                            mypassword, 0x01, 5, "C=AU;CN=theCA")
    print("X509.make_cert_self() returns:", n)
    assert (0 == n)
    assert (os.path.isfile(ca_certfile))
    print("Created new self-signed X.509 certificate '" + ca_certfile + "'")
    # Show its contents...
    _dump_and_print_x509(ca_certfile)

    # Generate a new RSA key pair for the user
    # (in practice, do this once)
    print("Generating a new RSA 1024-bit keypair for the USER...")
    user_prikeyfile = 'myuserprikey.p8'
    user_pubkeyfile = 'myuserpubkey.p1'
    n = Rsa.make_keys(user_pubkeyfile, user_prikeyfile, 1024,
                      Rsa.PublicExponent.RSAEXP_EQ_65537, mypassword)
    assert (0 == n)
    assert (os.path.isfile(ca_prikeyfile))
    assert (os.path.isfile(ca_pubkeyfile))

    # Use the user's public key as the subject of an X.509 cert issued by the
    # CA
    my_certfile = 'mycert.cer'
    n = X509.make_cert(my_certfile, ca_certfile, user_pubkeyfile, ca_prikeyfile, mypassword, 0x101, 4, "C=AU;CN=me",
                       extns="rfc822name=me@myorg.com;keyusage=digitalSignature,nonRepudiation;notBefore=2017-01-01")
    print("X509.make_cert() returns:", n)
    assert (0 == n)
    assert (os.path.isfile(my_certfile))
    print("Created X.509 certificate '" + my_certfile + "'")
    _dump_and_print_x509(my_certfile)

    # Create a Certificate Signing Request for the user
    my_csrfile = 'mycsr.p10'
    n = X509.cert_request(my_csrfile, user_prikeyfile, mypassword, "C=AU;CN=me;O=myorg",
                          extns="rfc822name=me.again@myorg.com;keyusage=dataEncipherment,keyAgreement;ipaddress=127.0.0.1")
    print("X509.cert_request() returns:", n)
    assert (0 == n)
    assert (os.path.isfile(my_csrfile))
    print("Created PKCS#10 certificate signing request '" + my_csrfile + "'")
    _dump_and_print_x509(my_csrfile)

    # Now use this CSR to create another X.509 cert issued by the CA
    # -- set `distname = ""` and pass the CSR file in the `subject_pubkeyfile` parameter
    my_certfilefromcsr = 'mycertfromcsr.cer'
    n = X509.make_cert(my_certfilefromcsr, ca_certfile, my_csrfile, ca_prikeyfile, mypassword, 0x102, 2, "",
                       sigalg=X509.SigAlg.RSA_SHA256)
    print("X509.make_cert() returns:", n)
    assert (0 == n)
    assert (os.path.isfile(my_certfilefromcsr))
    print("Created X.509 certificate '" + my_certfilefromcsr + "'")
    _dump_and_print_x509(my_certfilefromcsr)

    print("Check the keyUsage flags...")
    n = X509.key_usage_flags(my_certfilefromcsr)
    print("keyUsage bits: n =", format(n, "#08b"))
    mask = X509.KeyUsageFlags.DATAENCIPHERMENT
    print("n & KeyUsageFlags.DATAENCIPHERMENT =", bool(n & mask))
    mask = X509.KeyUsageFlags.KEYAGREEMENT
    print("n & KeyUsageFlags.KEYAGREEMENT =", bool(n & mask))
    mask = X509.KeyUsageFlags.CRLSIGN
    print("n & KeyUsageFlags.CRLSIGN =", bool(n & mask))

    # Create a Certificate Revocation List (CRL) revoking the cert made above with serial number 0x101
    # (Dates need to be hardcoded)
    ca_crlfile = 'theca.crl'
    revokedcertlist = "#x101,2020-04-25"
    n = X509.make_crl(ca_crlfile, ca_certfile, ca_prikeyfile, mypassword, revokedcertlist,
                      extns="thisUpdate=2020-04-25T00:01;nextUpdate=2020-12-31",
                      sigalg=X509.SigAlg.RSA_SHA256,
                      opts=X509.Opts.FORMAT_PEM)
    print("X509.make_crl() returns:", n)
    assert (0 == n)
    assert (os.path.isfile(ca_crlfile))
    print("Created CRL file '" + ca_crlfile + "'")
    _dump_and_print_x509(ca_crlfile)

    # Query the certificates we made above
    fname = ca_certfile
    query = 'subjectName'
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + fname + ", " + query + "):", res)

    query = 'isCA'
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + fname + ", " + query + "):", res)

    fname = my_certfile
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + fname + ", " + query + "):", res)

    fname = my_certfilefromcsr
    query = 'keyUsageString'
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + fname + ", " + query + "):", res)

    print("\nTry an invalid query string...")
    try:
        res = X509.query_cert(fname, 'badquery')
    except PKIError as e:
        print("(Expected) PKIError:", e)

    print("\nSee if our certificates have been revoked at any time...")
    # This cert has not been revoked
    fname = my_certfilefromcsr
    isrevoked = X509.cert_is_revoked(fname, ca_crlfile)
    print("X509.cert_is_revoked('" + fname + "') returns", isrevoked)
    assert (not isrevoked)

    # This cert was revoked on 2020-04-25 (yes, we can work in the future!)
    fname = my_certfile
    print(fname, X509.query_cert(fname, "serialNumber"))
    isrevoked = X509.cert_is_revoked(fname, ca_crlfile)
    print("X509.cert_is_revoked('" + fname + "') returns", isrevoked)
    assert (isrevoked)

    print("See if certificate was revoked on a certain date...")
    fname = my_certfile
    isodate = "2016-01-01"
    isrevoked = X509.cert_is_revoked(fname, ca_crlfile, isodate=isodate)
    print("X509.cert_is_revoked('" + fname + ", " + isodate + "') returns", isrevoked)
    assert (not isrevoked)

    print("\nRead in X.509 cert as a base64 string")
    s = X509.read_string_from_file(my_certfile)
    print(s)
    print("Now save from this string to a new file in PEM textual format...")
    fname = 'newcert.cer'
    n = X509.save_file_from_string(fname, s, in_pem_format=True)
    print("Created new cert file '" + fname + "'")
    assert (os.path.isfile(fname))
    _dump_file(fname)

    print("\nCheck if certs are valid now...")
    fname = 'AliceRSASignByCarl.cer'
    print("FILE:", fname)
    isvalid = X509.cert_is_valid_now(fname)
    s = X509.query_cert(fname, "NotAfter")
    print(s)

    print("X509.cert_is_valid_now('" + fname + "')=", isvalid)
    assert (isvalid)  # CAUTION: will not work after year 2039!
    fname = 'dims.cer'
    isvalid = X509.cert_is_valid_now(fname)
    print("X509.cert_is_valid_now('" + fname + "')=", isvalid)
    assert (not isvalid)

    print("\nCompute cert thumbprints...")
    fname = 'AliceRSASignByCarl.cer'
    print("FILE:", fname)
    thumb = X509.cert_thumb(fname)
    print("X509.cert_thumb(SHA-1):", thumb)
    assert (thumb == 'b30c48855055c2e64ce3196492d4b83831a6b3cb')

    thumb = X509.cert_thumb(fname, X509.HashAlg.SHA256)
    print("X509.cert_thumb(SHA-256):", thumb)


def test_x509_analyze():
    print("\nTESTING X.509 ANALYZE...")

    fname = 'AliceRSASignByCarl.cer'
    print("FILE:", fname)
    query = "serialNumber"
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + query + "):", res)
    print("Use `opts=X509.Opts.DECIMAL`...")
    res = X509.query_cert(fname, query, opts=X509.Opts.DECIMAL)
    print("X509.query_cert(" + query + "):", res)
    h = X509.cert_thumb(fname)
    print("cert_thumb():", h)
    h = X509.cert_hashissuersn(fname)
    print("hash(issuer+serialnumber):", h)

    fname = 'dims.cer'
    print("FILE:", fname)
    query = "issuerName"
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + query + "):", res)
    print("Use `opts=X509.Opts.LDAP`...")
    res = X509.query_cert(fname, query, opts=X509.Opts.LDAP)
    print("X509.query_cert(" + query + "):", res)

    fname = 'smallca.cer'
    print("FILE:", fname)
    query = "notAfter"
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + query + "):", res)
    query = "cRLDistributionPointsURI"
    res = X509.query_cert(fname, query)
    print("X509.query_cert(" + query + "):", res)

    # Test UTF-8-encoded output for a certificate with both Spanish and Chinese chars
    # CAUTION: these may not print properly in a console or may cause a 'UnicodeEncodeError' if stdout is redirected to a file
    fname = "maria-mx.cer"
    print("FILE:", fname)
    query = "issuerName"
    res = X509.query_cert(fname, query, opts=X509.Opts.UTF8)
    print("X509.query_cert(" + query + "):", res)
    query = "subjectName"
    res = X509.query_cert(fname, query, opts=X509.Opts.UTF8)
    print("X509.query_cert(" + query + "):", res)
    print(X509.text_dump_tostring(fname, opts=X509.Opts.UTF8))

    # Extract the public key from the X.509 cert
    keystr = Rsa.read_public_key(fname)
    print("Public key bits:", Rsa.key_bits(keystr))
    hcode = Rsa.key_hashcode(keystr)
    print("Rsa.key_hashcode():", hcode)
    h = X509.cert_thumb(fname, X509.HashAlg.MD5)
    print("X509.cert_thumb(MD5):", h)
    h = X509.cert_hashissuersn(fname)
    print("hash(issuer+serialnumber):", h)


def test_x509_validate():
    print("\nTESTING X.509 VALIDATE...")

    print("1. A valid certificate and its issuer:")
    certfile = "AliceRSASignByCarl.cer"
    issuerfile = "CarlRSASelf.cer"
    print("CERTFILE:", certfile)
    print("ISSUERFILE:", issuerfile)

    print("Is cert valid now?")
    isok = X509.cert_is_valid_now(certfile)
    print("cert_is_valid_now:", isok)
    # This will fail in the year 2040 :-)
    assert (isok)

    print("Was cert signed by issuer?")
    isok = X509.cert_is_verified(certfile, issuerfile)
    print("cert_is_verified:", isok)
    assert (isok)

    print("Validate the certificate path...")
    certlist = certfile + ";" + issuerfile
    print("CERTLIST:", certlist)
    isok = X509.cert_path_is_valid(certlist)
    print("cert_path_is_valid:", isok)
    assert (isok)

    print("2. A valid but expired certificate and its issuer:")
    certfile = "dims.cer"
    issuerfile = "UTNUSERFirst-Object.cer"
    print("CERTFILE:", certfile)
    print("ISSUERFILE:", issuerfile)

    print("Is cert valid now?")
    d = X509.query_cert(certfile, "notAfter")
    print("  X509.query_cert('notAfter'):", d)
    isok = X509.cert_is_valid_now(certfile)
    print("cert_is_valid_now:", isok, "(expected False)")
    # This will fail if you go back in time to before Nov 2011 :-)
    assert (not isok)

    print("Was cert signed by issuer?")
    isok = X509.cert_is_verified(certfile, issuerfile)
    print("cert_is_verified:", isok)
    assert (isok)

    print("Validate the certificate path...")
    certlist = certfile + ";" + issuerfile
    print("CERTLIST:", certlist)

    print("a) This will fail because a cert has expired...")
    try:
        isok = X509.cert_path_is_valid(certlist)
    except PKIError as e:
        print("(Expected):", e)

    print("b) Now try again with X509.Opts.NO_TIMECHECK...")
    isok = X509.cert_path_is_valid(certlist, no_timecheck=True)
    print("cert_path_is_valid(NO_TIMECHECK):", isok)

    print("3. A valid certificate but the wrong issuer:")
    certfile = "AliceRSASignByCarl.cer"
    issuerfile = "UTNUSERFirst-Object.cer"
    print("CERTFILE:", certfile)
    print("ISSUERFILE:", issuerfile)

    print("Was cert signed by issuer?")
    isok = X509.cert_is_verified(certfile, issuerfile)
    print("cert_is_verified:", isok, "(expected False)")
    assert (not isok)


def test_x509_extract():
    print("\nTESTING X.509 EXTRACT...")

    print("Extract cert files from a P7 chain file")
    p7file = "bob.p7b"
    print("P7 FILE:", p7file)
    n = X509.get_cert_count_from_p7(p7file)
    print("X509.get_cert_count_from_p7()=", n)
    assert (n > 0)
    # Extract each cer file from p7 file
    for i in range(1, n + 1):
        print("Count:", i)
        fname = "bobcert" + str(i) + ".cer"
        print(" OUTFILE:", fname)
        r = X509.get_cert_from_p7(fname, p7file, i)
        print(" X509.get_cert_from_p7() returns:", r)
        assert (r > 0)
        print(" X509_thumb():", X509.cert_thumb(fname))

    print("Extract cert files from a PFX (p12) file")
    pfxfile = "alice.pfx"
    print("PFX FILE:", pfxfile)
    fname = 'alice_cert.cer'
    print(" OUTFILE:", fname)
    r = X509.get_cert_from_pfx(fname, pfxfile, "password")
    assert (r > 0)
    print(" ASN1 TYPE(" + fname + ")=" + Asn1.type(fname))
    print(" X509_thumb():", X509.cert_thumb(fname))
    # Show thumbprints of known certificate files...
    print("X509_thumb(Carl): ", X509.cert_thumb("CarlRSASelf.cer"))
    print("X509_thumb(Alice):", X509.cert_thumb("AliceRSASignByCarl.cer"))
    print("X509_thumb(Bob):  ", X509.cert_thumb("BobRSASignByCarl.cer"))

    print("Extract all cert files as P7 chain from a PFX file")
    pfxfile = "alice.pfx"
    print("PFX FILE:", pfxfile)
    fname = 'alice_certs.p7'
    print(" OUTFILE:", fname)
    r = X509.get_p7chain_from_pfx(fname, pfxfile, "password")
    assert (r > 0)
    print(" ASN1 TYPE(" + fname + ")=" + Asn1.type(fname))


def test_rng():
    print("\nTESTING RANDOM NUMBER GENERATOR...")

    # Initialize from seed file. File is created if it does not exist.
    # Optional but recommended for extra security
    seedfile = 'myseedfile.dat'
    n = Rng.initialize(seedfile)
    assert (0 == n)
    print('Rng.initialize() returns', n, ". Contents of seed file:")
    sd = read_binary_file(seedfile)
    print(Cnv.tohex(sd))
    assert (len(sd) == Rng.SEED_BYTES)

    print("5 random byte arrays")
    for i in range(5):
        b = Rng.bytestring((i + 2) * 2)
        print(Cnv.tohex(b).lower())

    print("5 random numbers in the range [-1 million, +1 million]")
    for i in range(5):
        r = Rng.number(-1000000, 1000000)
        print(r)
        assert (-1000000 <= r and r <= 1000000)

    print("5 random octet values")
    s = ""  # fudge to do in one line
    for i in range(5):
        r = Rng.octet()
        assert (0 <= r and r <= 255)
        s += str(r) + " "
    print(s)

    # Update seedfile
    n = Rng.update_seedfile(seedfile)
    assert (0 == n)
    print('Rng.update_seedfile() returns', n, ". Contents of seed file:")
    sd = read_binary_file(seedfile)
    print(Cnv.tohex(sd))
    assert (len(sd) == Rng.SEED_BYTES)


def test_hash():
    print("\nTESTING Hash...")
    # write a file containing the 3 bytes 'abc'
    write_text_file('abc.txt', 'abc')
    _dump_file('abc.txt')
    abc_hex = Cnv.tohex(b'abc')
    print("'abc' in hex:", abc_hex)

    # Use default SHA-1 algorithm
    print("Using default SHA-1...")
    b = Hash.data(b'abc')
    print("Hash.data('abc'):", Cnv.tohex(b))
    h = Hash.hex_from_data(b'abc')
    print("Hash.hex_from_data('abc'):", h)
    h = Hash.hex_from_data(bytearray.fromhex('616263'))
    print("Hash.hex_from_data('abc'):", h)
    h = Hash.hex_from_hex(abc_hex)
    print("Hash.hex_from_hex(abc_hex):", h)
    b = Hash.file('abc.txt')
    print("Hash.file('abc.txt'):", Cnv.tohex(b))
    h = Hash.hex_from_file('abc.txt')
    print("Hash.hex_from_file('abc.txt'):", h)

    print("Using SHA-256...")
    b = Hash.data(b'abc', Hash.Alg.SHA256)
    print("Hash.data('abc'):", Cnv.tohex(b))
    h = Hash.hex_from_hex(abc_hex, Hash.Alg.SHA256)
    print("Hash.hex_from_hex(abc_hex):", h)
    b = Hash.file('abc.txt', Hash.Alg.SHA256)
    print("Hash.file('abc.txt'):", Cnv.tohex(b))
    h = Hash.hex_from_file('abc.txt', Hash.Alg.SHA256)
    print("Hash.hex_from_file('abc.txt'):", h)

    # compute SHA256(SHA256('abc')) using Hash.double()
    b = Hash.double(b'abc', Hash.Alg.SHA256)
    print("Hash.double('abc',SHA256):", Cnv.tohex(b))
    # and again by composition
    b2 = Hash.data(Hash.data(b'abc', Hash.Alg.SHA256),
                   Hash.Alg.SHA256)
    print("SHA256(SHA256('abc')):    ", Cnv.tohex(b2))


def test_hash_sha3():
    print("\nTESTING Hash(SHA3)...")
    # write a file containing the 3 bytes 'abc'
    write_text_file('abc.txt', 'abc')
    _dump_file('abc.txt')
    abc_hex = Cnv.tohex(b'abc')
    print("'abc' in hex:", abc_hex)

    b = Hash.data(b'abc', Hash.Alg.SHA3_224)
    print("Hash.data('abc'):", Cnv.tohex(b))
    assert (b == Cnv.fromhex('e642824c3f8cf24ad09234ee7d3c766fc9a3a5168d0c94ad73b46fdf'))
    h = Hash.hex_from_hex(abc_hex, Hash.Alg.SHA3_256)
    print("Hash.hex_from_hex(abc_hex):", h)
    assert (Cnv.fromhex(h) == Cnv.fromhex('3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532'))
    b = Hash.file('abc.txt', Hash.Alg.SHA3_384)
    print("Hash.file('abc.txt'):", Cnv.tohex(b))
    assert (b == Cnv.fromhex(
        'ec01498288516fc926459f58e2c6ad8df9b473cb0fc08c2596da7cf0e49be4b298d88cea927ac7f539f1edf228376d25'))
    h = Hash.hex_from_file('abc.txt', Hash.Alg.SHA3_512)
    print("Hash.hex_from_file('abc.txt'):", h)
    assert (Cnv.fromhex(h) == Cnv.fromhex(
        'b751850b1a57168a5693cd924b6b096e08f621827444f70d884f5d0240d2712e10e116e9192af3c91a7ec57647e3934057340b4cf408d5a56592f8274eec53f0'))


def test_hmac():
    print("\nTESTING Hmac...")
    print("Test case 4 from RFC 2202 and RFC 4231")
    key = Cnv.fromhex('0102030405060708090a0b0c0d0e0f10111213141516171819')
    print("key: ", Cnv.tohex(key))
    # data = 0xcd repeated 50 times
    data = bytearray([0xcd] * 50)
    print("data:", Cnv.tohex(data))

    b = Hmac.data(data, key)
    print("HMAC-SHA-1:  ", Cnv.tohex(b))
    assert (b == Cnv.fromhex('4c9007f4026250c6bc8414f9bf50c86c2d7235da'))

    b = Hmac.data(data, key, Hmac.Alg.MD5)
    print("HMAC-MD5:    ", Cnv.tohex(b))
    assert (b == Cnv.fromhex('697eaf0aca3a3aea3a75164746ffaa79'))

    b = Hmac.data(data, key, Hmac.Alg.SHA256)
    print("HMAC-SHA-256:", Cnv.tohex(b))
    assert (b == Cnv.fromhex(
        '82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b'))

    h = Hmac.hex_from_data(data, key, Hmac.Alg.SHA256)
    print("HMAC-SHA-256:", h)
    assert (h == '82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b')

    b = Hmac.data(data, key, Hmac.Alg.SHA512)
    print("HMAC-SHA-512:", Cnv.tohex(b))
    assert (b == Cnv.fromhex(
        'b0ba465637458c6990e5a8c5f61d4af7 e576d97ff94b872de76f8050361ee3db a91ca5c11aa25eb4d679275cc5788063 a5f19741120c4f2de2adebeb10a298dd'))

    print("Test case 7 from RFC 4231")
    key = bytearray([0xaa] * 131)
    print("key: ", Cnv.tohex(key).lower())
    data = b"This is a test using a larger than block-size key and a larger than block-size data. The key needs to be hashed before being used by the HMAC algorithm."
    print("data:", data)
    b = Hmac.data(data, key, Hmac.Alg.SHA224)
    print("HMAC-SHA-224:", Cnv.tohex(b))
    assert (b == Cnv.fromhex(
        '3a854166ac5d9f023f54d517d0b39dbd946770db9c2b95c9f6f565d1'))

    # HMAC hex <-- hex
    print("Test case 1 from RFC 2202 and RFC 4231")
    keyhex = "0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b"  # (20 bytes)
    datahex = "4869205468657265"  # ("Hi There")
    print("key: ", keyhex)
    print("data:", datahex)
    h = Hmac.hex_from_hex(datahex, keyhex)
    print("HMAC-SHA-1:", h)
    assert (h == "b617318655057264e28bc0b6fb378c8ef146be00")
    h = Hmac.hex_from_hex(datahex, keyhex, Hmac.Alg.SHA256)
    print("HMAC-SHA-256:", h)
    assert (h == "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")


def test_hmac_sha3():
    print("\nTESTING Hmac(SHA-3)...")
    print("NIST HMAC_SHA3-256.pdf Sample #1")
    key = Cnv.fromhex('000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F')
    print("key: ", Cnv.tohex(key))
    data = b'Sample message for keylen<blocklen'
    print("data:", data.decode())
    b = Hmac.data(data, key, Hmac.Alg.SHA3_256)
    print("HMAC-SHA-3-256:", Cnv.tohex(b))
    assert (b == Cnv.fromhex('4fe8e202c4f058e8dddc23d8c34e467343e23555e24fc2f025d598f558f67205'))

    print("NIST HMAC_SHA3-512.pdf Sample #3")
    key = Cnv.fromhex("""000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F
202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F
404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F
606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F
8081828384858687""")
    print("key: ", Cnv.tohex(key))
    data = b'Sample message for keylen>blocklen'
    print("data:", data.decode())
    b = Hmac.data(data, key, Hmac.Alg.SHA3_512)
    print("HMAC-SHA-3-512:", Cnv.tohex(b))
    assert (b == Cnv.fromhex(
        '5f464f5e5b7848e3885e49b2c385f0694985d0e38966242dc4a5fe3fea4b37d46b65ceced5dcf59438dd840bab22269f0ba7febdb9fcf74602a35666b2a32915'))


def test_wipe():
    print("\nTESTING Wipe...")

    print("Note that Wipe.data() just zeroizes the data, it does not change the length")

    b = Cnv.fromhex('3a854166ac5d9f023f54d517d0b39dbd946770db9c2b95c9f6f565d1')
    print("BEFORE            b=", Cnv.tohex(b))
    Wipe.data(b)
    print("AFTER Wipe.data() b=", Cnv.tohex(b))
    print("AFTER Wipe.data()", str(b))
    print([c for c in b])
    assert all([c == 0 for c in b])

    # works with a bytes type but not with an immutable string type
    s = b"a string"
    print("BEFORE            s='" + str(s) + "'")
    print([c for c in s])
    Wipe.data(s)
    print("AFTER Wipe.data()", str(s))
    print([c for c in s])
    assert all([c == 0 for c in s])

    # write a file containing some text
    fname = 'tobedeleted.txt'
    write_text_file(fname, 'Some secret text in this file.')
    _dump_file(fname)
    assert (os.path.isfile(fname))
    Wipe.file(fname)
    print("After Wipe.file(), isfile() returns", os.path.isfile(fname))
    assert (not os.path.isfile(fname))


def test_asn1():
    print("\nTESTING ASN.1...")
    fname = "smallca.cer"
    print("FILE:", fname)
    t = Asn1.type(fname)
    print("Asn1.type():", t)
    dumpfile = 'asn1dump.txt'
    Asn1.text_dump(dumpfile, fname, opts=Asn1.Opts.ADDLEVELS)
    print("Asn1.text_dump():")
    _print_file(dumpfile)


def test_ocsp():
    print("\nTESTING Ocsp...")
    # Create an OCSP request to check a code-signing certificate issued by the holder
    # of certificate in the file `UTNUSERFirst-Object.cer`
    issuercert = "UTNUSERFirst-Object.cer"
    print("Issuer Cert=", issuercert)
    certfile = "dims.cer"
    print("Cert File to check=", certfile)
    req = Ocsp.make_request(issuercert, certfile)
    print("OCSPRequest=", req)
    assert len(req) > 0
    # We can analyze the ASN.1 data structure from the base64 string
    _dump_and_print_asn1(req)

    # Pass a hex serial number instead of filename
    serialnum = "#x 00 FB C7 23 22 8C 8C 80 22 D8 85 92 23 DE E7 06 60"
    print("Cert SerialNumber=", serialnum)
    req1 = Ocsp.make_request(issuercert, serialnum)
    print("OCSPRequest=", req1)
    # These should be the same
    assert (req1 == req)

    # Now read a response
    responsefile = "ocsp_response_ok_dims.dat"
    print("ResponseFile=", responsefile)
    resp = Ocsp.read_response(responsefile, issuercert)
    print("OCSPResponse:", resp)


def test_ecc():
    print("\nTESTING Ecc...")
    pubkeyfile = "myeckeyp256.pub"
    prikeyfile = "myeckeyp256.p8"
    password = "password"
    curvename = "P-256"
    # Create a new pair of ECC keys, saved as DER-encoded files
    n = Ecc.make_keys(pubkeyfile, prikeyfile, curvename, password)
    assert (0 == n)
    _dump_and_print_asn1(pubkeyfile)
    print(pubkeyfile + ": " + Asn1.type(pubkeyfile))
    print(prikeyfile + ": " + Asn1.type(prikeyfile))

    # Read in private key to an internal key string
    intpristr = Ecc.read_private_key(prikeyfile, password)
    # This will be different each time, even for the same key
    print(intpristr)
    # But the key hash code will be the same
    print("key_hash_code =", Ecc.key_hashcode(intpristr))

    # Query this string for info
    query = "keyBits"
    r = Ecc.query_key(intpristr, query)
    print("Ecc.query_key(" + query + ")=", r)
    query = "curveName"
    r = Ecc.query_key(intpristr, query)
    print("Ecc.query_key(" + query + ")=", r)
    query = "privateKey"
    r = Ecc.query_key(intpristr, query)
    print("Ecc.query_key(" + query + ")=", r)

    # Read in a key from its hex representation
    print("A NIST P-192 public key in X9.63 uncompressed format")
    keyhex = "0496C248BE456192FA1380CCF615D171452F41FF31B92BA733524FD77168DEA4425A3EA8FD79B98DC7AFE83C86DCC39A96"
    curvename = "prime192v1"  # A synonym for "P-192"
    print("KEYHEX:", keyhex)
    print("CURVE: ", curvename)
    intpubstr = Ecc.read_key_by_curve(keyhex, curvename)
    print("keyBits=", Ecc.query_key(intpubstr, "keyBits"))
    f = Ecc.query_key(intpubstr, "isPrivate")
    print("isPrivate=", f)
    assert (not f)

    print("A Bitcoin private key in base58 form")
    keyb58 = "6ACCbmy9qwiFcuVgvxNNwMPfoghobzznWrLs3v7t3RmN"
    curvename = "secp256k1"
    print("KEYB58:", keyb58)
    print("CURVE: ", curvename)
    intpristr = Ecc.read_key_by_curve(
        Cnv.tohex(Cnv.frombase58(keyb58)), curvename)
    print("keyBits=", Ecc.query_key(intpristr, "keyBits"))
    f = Ecc.query_key(intpristr, "isPrivate")
    print("isPrivate=", f)
    assert (f)
    print("key_hash_code =", Ecc.key_hashcode(intpristr))

    print("Extract the public key in hex form from the internal private key string")
    pubkey = Ecc.query_key(intpristr, 'publicKey')
    print("publicKey=", pubkey)
    assert pubkey == '04654bacc2fc7a3bde0f8eb95dc5aac9ba1df732255cf7f2eb7e1e8e6edbb1f4188ff3752ac4bdf1e3a31a488747745dddcbabd33a10c3b52d737c092851da13c0'

    print("Extract the public key as an internal key string")
    intpubstr = Ecc.publickey_from_private(intpristr)
    print("intpubstr=", intpubstr)
    print("key_hash_code =", Ecc.key_hashcode(intpubstr))

    print("Query this internal public key string...")
    query = "keybits"
    print("Ecc.query_key(" + query + ")=", Ecc.query_key(intpubstr, query))
    query = "curvename"
    print("Ecc.query_key(" + query + ")=", Ecc.query_key(intpubstr, query))
    query = "isPrivate"
    print("Ecc.query_key(" + query + ")=", Ecc.query_key(intpubstr, query))

    print("Save keys in various new file forms...")
    # Note we must save from the internal key string forms
    # Default unencrypted key files...
    newkeyfile = 'myecpublic.key'
    n = Ecc.save_key(newkeyfile, intpubstr)
    # Show what type of file we made
    print("File:", newkeyfile, "-->", Asn1.type(newkeyfile))
    # and read it back in to check it's really OK...
    s = Ecc.read_public_key(newkeyfile)
    assert (Ecc.query_key(s, 'keyBits') == 256)

    newkeyfile = 'myecprivate.key'
    n = Ecc.save_key(newkeyfile, intpristr)
    print("File:", newkeyfile, "-->", Asn1.type(newkeyfile))
    s = Ecc.read_private_key(newkeyfile)
    assert (Ecc.query_key(s, 'keyBits') == 256)

    # Alternative PKCS#8 key type (unencrypted)
    newkeyfile = 'myecprivate.p8'
    n = Ecc.save_key(newkeyfile, intpristr,
                     keytype=Ecc.KeyType.PKCS8, fileformat=Ecc.Format.PEM)
    print("File:", newkeyfile, "-->", Asn1.type(newkeyfile))
    s = Ecc.read_private_key(newkeyfile)
    assert (Ecc.query_key(s, 'keyBits') == 256)

    # Encrypted private key (always PKCS#8)
    newkeyfile = 'myecprivate_enc.p8'
    n = Ecc.save_enc_key(newkeyfile, intpristr, 'password')
    print("File:", newkeyfile, "-->", Asn1.type(newkeyfile))
    s = Ecc.read_private_key(newkeyfile, 'password')
    assert (Ecc.query_key(s, 'keyBits') == 256)

    # with stronger encryption
    newkeyfile = 'myecprivate_encx.p8'
    n = Ecc.save_enc_key(newkeyfile, intpristr, 'password',
                         pbescheme=Ecc.PbeScheme.PBKDF2_AES256,
                         params="count=5999;prf=hmacWithSHA256;")
    print("File:", newkeyfile, "-->", Asn1.type(newkeyfile))
    s = Ecc.read_private_key(newkeyfile, 'password')
    assert (Ecc.query_key(s, 'keyBits') == 256)
    # Dump this
    _dump_and_print_asn1(newkeyfile)


def test_ecc_brainpool():
    print("\nTESTING ECC BRAINPOOL...")
    pubkeyfile = "myeckeyBrainpool384.pub"
    prikeyfile = "myeckeyBrainpool384.p8e"
    password = "password"
    curvename = "brainpoolP384r1"
    # Create a new pair of ECC keys, saved as DER-encoded files with stronger encryption
    n = Ecc.make_keys(pubkeyfile, prikeyfile, curvename, password,
                      Ecc.PbeScheme.PBKDF2_AES256, "count=8999;prf=hmacWithSha512", Ecc.Format.PEM)
    assert (0 == n)
    _dump_and_print_asn1(pubkeyfile)
    print(pubkeyfile + ": " + Asn1.type(pubkeyfile))
    print(prikeyfile + ": " + Asn1.type(prikeyfile))

    # Read in private key to an internal key string
    intpristr = Ecc.read_private_key(prikeyfile, password)
    # This will be different each time, even for the same key
    print(intpristr)
    # But the key hash code will be the same
    print("pri_key_hash_code =", Ecc.key_hashcode(intpristr))
    print("pub_key_hash_code =", Ecc.key_hashcode(Ecc.read_public_key(pubkeyfile)))

    # Query this string for info
    query = "keyBits"
    r = Ecc.query_key(intpristr, query)
    print("Ecc.query_key(" + query + ")=", r)
    query = "curveName"
    r = Ecc.query_key(intpristr, query)
    print("Ecc.query_key(" + query + ")=", r)
    query = "privateKey"
    r = Ecc.query_key(intpristr, query)
    print("Ecc.query_key(" + query + ")=", r)

    print("Sign 'abc' using ECDSA...")
    msg = b'abc'
    print("MSG =", Cnv.tohex(msg))
    # Compute the signature value NB this will be different each time because we use a new key each time
    sigval = Sig.sign_data(msg, intpristr, "", Sig.Alg.ECDSA_SHA384, Sig.Opts.DETERMINISTIC)
    print("SIG =", sigval)
    # Verify the signature
    isok = Sig.data_is_verified(sigval, msg, pubkeyfile, Sig.Alg.ECDSA_SHA384)
    print("Sig.data_is_verified returns ", isok)


def test_ecc_dh_shared_secret():
    print("\nTEST ECC DIFFIE-HELLMAN SHARED SECRET...")

    '''
    Ref: CAVS 14.1 ECC CDH Primitive (SP800 - 56A Section 5.7.1.2) Test Information for "testecccdh"
    https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/components/ecccdhtestvectors.zip  
    Extract:
    ----------------------------------------
    [P-256]
    
    COUNT = 0
    QCAVSx = 700c48f77f56584c5cc632ca65640db91b6bacce3a4df6b42ce7cc838833d287
    QCAVSy = db71e509e3fd9b060ddb20ba5c51dcc5948d46fbf640dfe0441782cab85fa4ac
    dIUT = 7d7dc5f71eb29ddaf80d6214632eeae03d9058af1fb6d22ed80badb62bc1a534
    QIUTx = ead218590119e8876b29146ff89ca61770c4edbbf97d38ce385ed281d8a6b230
    QIUTy = 28af61281fd35e2fa7002523acc85a429cb06ee6648325389f59edfce1405141
    ZIUT = 46fc62106420ff012e54a434fbdd2d25ccc5852060561e68040dd7778997bd7b
    --------------------------------------
    '''
    # Read in private key (dIUT)
    prikeystr = Ecc.read_key_by_curve("7d7dc5f71eb29ddaf80d6214632eeae03d9058af1fb6d22ed80badb62bc1a534",
                                      Ecc.CurveName.P_256)
    # Compose public key from QCAVSx+y in hex form
    pubkeyhex = "04" + "700c48f77f56584c5cc632ca65640db91b6bacce3a4df6b42ce7cc838833d287" \
                + "db71e509e3fd9b060ddb20ba5c51dcc5948d46fbf640dfe0441782cab85fa4ac"
    pubkeystr = Ecc.read_key_by_curve(pubkeyhex, Ecc.CurveName.P_256)
    # Compute shared secret
    zz = Ecc.dh_shared_secret(prikeystr, pubkeystr)
    print("Computed DH shared secret =", Cnv.tohex(zz))
    # Compare to expected result (ZIUT)
    okhex = "46fc62106420ff012e54a434fbdd2d25ccc5852060561e68040dd7778997bd7b"
    print("Expected DH shared secret =", okhex)
    assert (Cnv.tohex(zz).lower() == okhex.lower())


def test_ecc_dh_shared_secret_x25519():
    print("\nTEST X25519 ECDH DIFFIE-HELLMAN SHARED SECRET...")

    '''
    // Ref: RFC7748 Section 6.1
    // https://tools.ietf.org/html/rfc7748#section-6.1

    Test vector:

    Alice's private key, a:
        77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a
    Alice's public key, X25519(a, 9):
        8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a
    Bob's private key, b:
        5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb
    Bob's public key, X25519(b, 9):
        de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f
    Their shared secret, K:
        4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742
    '''
    okhex = "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"

    # NOTE: for X25519 curve keys we must specify private or public (because they are both the same length)
    # Read in Alice's private key
    prikeystr = Ecc.read_key_by_curve("77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a",
                                      Ecc.CurveName.X25519, ispublic=False)
    # Read in Bob's public key
    pubkeystr = Ecc.read_key_by_curve("de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f",
                                      Ecc.CurveName.X25519, ispublic=True)
    print("Our private key: ", Ecc.query_key(prikeystr, "privateKey"))
    print("Their public key:", Ecc.query_key(pubkeystr, "publicKey"))
    # Compute shared secret
    zz = Ecc.dh_shared_secret(prikeystr, pubkeystr)
    print("Computed DH shared secret =", Cnv.tohex(zz))
    # Compare to expected result
    print("Expected DH shared secret =", okhex)
    assert (Cnv.tohex(zz).lower() == okhex.lower())

    # OTHER WAY AROUND
    # Read in Bobs's private key
    prikeystr = Ecc.read_key_by_curve("5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb",
                                      Ecc.CurveName.X25519, ispublic=False)
    # Read in Alice's public key
    pubkeystr = Ecc.read_key_by_curve("8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a",
                                      Ecc.CurveName.X25519, ispublic=True)
    print("Our private key: ", Ecc.query_key(prikeystr, "privateKey"))
    print("Their public key:", Ecc.query_key(pubkeystr, "publicKey"))
    # Compute shared secret
    zz = Ecc.dh_shared_secret(prikeystr, pubkeystr)
    print("Computed DH shared secret =", Cnv.tohex(zz))
    # Compare to expected result
    print("Expected DH shared secret =", okhex)
    assert (Cnv.tohex(zz).lower() == okhex.lower())


def test_ecc_dh_shared_secret_x448():
    print("\nTEST X448 ECDH DIFFIE-HELLMAN SHARED SECRET...")

    '''
	// Ref: RFC7748 Section 6.2
	// https://tools.ietf.org/html/rfc7748#section-6.2

	Test vector:

	Alice's private key, a:
	9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28d
	d9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b
	Alice's public key, X448(a, 5):
	9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c
	22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0
	Bob's private key, b:
	1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d
	6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d
	Bob's public key, X448(b, 5):
	3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b430
	27d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609
	Their shared secret, K:
	07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282b
	b60c0b56fd2464c335543936521c24403085d59a449a5037514a879d
    '''
    okhex = "07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282bb60c0b56fd2464c335543936521c24403085d59a449a5037514a879d"

    # Read in Alice's private key
    prikeystr = Ecc.read_key_by_curve(
        "9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28dd9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b",
        Ecc.CurveName.X448, ispublic=False)
    # Read in Bob's public key
    pubkeystr = Ecc.read_key_by_curve(
        "3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b43027d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609",
        Ecc.CurveName.X448, ispublic=True)
    print("Our private key: ", Ecc.query_key(prikeystr, "privateKey"))
    print("Their public key:", Ecc.query_key(pubkeystr, "publicKey"))
    # Compute shared secret
    zz = Ecc.dh_shared_secret(prikeystr, pubkeystr)
    print("Computed DH shared secret =", Cnv.tohex(zz))
    # Compare to expected result
    print("Expected DH shared secret =", okhex)
    assert (Cnv.tohex(zz).lower() == okhex.lower())

    # OTHER WAY AROUND
    # Read in Bobs's private key
    prikeystr = Ecc.read_key_by_curve(
        "1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d",
        Ecc.CurveName.X448, ispublic=False)
    # Read in Alice's public key
    pubkeystr = Ecc.read_key_by_curve(
        "9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0",
        Ecc.CurveName.X448, ispublic=True)
    print("Our private key: ", Ecc.query_key(prikeystr, "privateKey"))
    print("Their public key:", Ecc.query_key(pubkeystr, "publicKey"))
    # Compute shared secret
    zz = Ecc.dh_shared_secret(prikeystr, pubkeystr)
    print("Computed DH shared secret =", Cnv.tohex(zz))
    # Compare to expected result
    print("Expected DH shared secret =", okhex)
    assert (Cnv.tohex(zz).lower() == okhex.lower())


def test_pbe():
    print("\nTESTING PASSWORD-BASED ENCRYPTION (PBE)...")
    password = 'password'
    salt = Cnv.fromhex('78 57 8E 5A 5D 63 CB 06')
    count = 2048
    print("password = '" + password + "'")
    print("salt = 0x" + Cnv.tohex(salt))
    print("count =", count)

    dklen = 24
    print("dklen =", dklen)
    dk = Pbe.kdf2(dklen, password, salt, count)
    print("dk =", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == "BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643"

    # Same params but derive a longer key (CAUTION: never use the same salt in
    # practice)
    dklen = 64
    print("dklen =", dklen)
    dk = Pbe.kdf2(dklen, password, salt, count)
    print("dk =", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == \
           "BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643C4B150DEF77511224479994567F2E9B4E3BD0DF7AEDA3022B1F26051D81505C794F8940C04DF1144"

    # Use different HMAC algorithms
    dklen = 24
    dk = Pbe.kdf2(dklen, password, salt, count, prfalg=Pbe.PrfAlg.HMAC_SHA1)
    print("dk(HMAC-SHA-1)   =", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == "BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643"
    dk = Pbe.kdf2(dklen, password, salt, count, prfalg=Pbe.PrfAlg.HMAC_SHA256)
    print("dk(HMAC-SHA-256) =", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == "97B5A91D35AF542324881315C4F849E327C4707D1BC9D322"
    dk = Pbe.kdf2(dklen, password, salt, count, prfalg=Pbe.PrfAlg.HMAC_SHA224)
    print("dk(HMAC-SHA-224) =", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == "10CFFEDFB13503519969151E466F587028E0720B387F9AEF"


def test_pfx():
    print("\nTESTING PFX (PKCS#12) FILE FUNCTIONS...")
    pfxfile = "bob1.pfx"
    certlist = "BobRSASignByCarl.cer"
    prikeyfile = "BobPrivRSAEncrypt.p8e"
    n = Pfx.make_file(pfxfile, certlist, prikeyfile, 'password', "Bob's ID")
    assert (0 == n)
    print("Created new PKCS#12 file:", pfxfile)
    print("Asn1.Type(" + pfxfile + ") -->", Asn1.type(pfxfile))

    print("Check signature is valid against password...")
    isvalid = Pfx.sig_is_valid(pfxfile, 'password')
    print("isvalid=", isvalid)
    assert (isvalid)

    print("Use the wrong password...")
    isvalid = Pfx.sig_is_valid(pfxfile, 'passwordXXX')
    print("isvalid=", isvalid)
    assert (not isvalid)

    print("Extract private key file from Pfx...")
    newp8file = "NewBobPrivRsa.p8e"
    n = Rsa.get_privatekey_from_pfx(newp8file, pfxfile)
    assert (n > 0)
    print("Created new PKCS#8 file:", newp8file)
    print("Asn1.Type(" + newp8file + ") -->", Asn1.type(newp8file))


def test_pem():
    print("\nTESTING PEM/BINARY FILE CONVERSIONS...")
    binfile = "smallca.cer"
    pemfile = "smallca.pem"

    print("Create a PEM-format CERTIFICATE file from binary file...")
    print("Binary file:", binfile)
    n = Pem.from_binfile(pemfile, binfile, "CERTIFICATE", Pem.EOL.UNIX)
    assert (0 == n)
    print("Created file:", pemfile)
    print("Check certificate thumbprints...")
    thumb_bin = X509.cert_thumb(binfile)
    thumb_pem = X509.cert_thumb(pemfile)
    print("X509.cert_thumb(" + binfile + ")=" + thumb_bin)
    print("X509.cert_thumb(" + pemfile + ")=" + thumb_pem)
    assert (thumb_bin == thumb_pem)

    print("Convert PEM to binary...")
    binfile2 = "smallca-copy.bin"
    n = Pem.to_binfile(binfile2, pemfile)
    assert (0 == n)
    print("Created file:", binfile2)
    print("Binary files should be identical...")
    hash_bin1 = Hash.hex_from_file(binfile)
    hash_bin2 = Hash.hex_from_file(binfile2)
    print("Hash.hex_from_file(" + binfile + ")=\t" + hash_bin1)
    print("Hash.hex_from_file(" + binfile2 + ")=\t" + hash_bin2)
    assert (hash_bin1 == hash_bin2)
    # Note that the *hash* of the PEM file is not the same as the hash of the binary,
    # but the X509.cert_thumb() is the same for both.


def test_cms_envdata():
    print("\nTESTING CMS ENV-DATA...")
    print("Creating an enveloped-data message for Bob and Carl, using file-->file mode")
    # Create a file
    mytext = 'This is some sample content.'
    myfile = "mycontent.txt"
    write_text_file(myfile, mytext)
    envdatafile = 'cms2bobandcarl.p7m'
    certlist = "BobRSASignByCarl.cer;CarlRSASelf.cer"
    n = Cms.make_envdata(envdatafile, myfile, certlist)
    print("Cms.make_envdata() returns " + str(n) + " (expected 2 = # of recipients)")
    assert (n > 0)
    _dump_and_print_asn1(envdatafile)
    print("Asn1.type('" + envdatafile + "')-->" + Asn1.type(envdatafile))

    # Query this CMS object file
    fname = envdatafile
    query = "recipientIssuerName"
    res = Cms.query_envdata(envdatafile, query)
    print("Cms.query_envdata(" + fname + ", " + query + "):", res)
    query = "iv"
    res = Cms.query_envdata(envdatafile, query)
    print("Cms.query_envdata(" + fname + ", " + query + "):", res)

    print("Bob reads the message, outputting to a new file")
    outputfile = "bobsdata.txt"
    # Bob reads in his private key to a secure "internal" key string
    prikeystr = Rsa.read_private_key('BobPrivRSAEncrypt.p8e', 'password')
    n = Cms.read_envdata_to_file(outputfile, envdatafile, prikeystr)
    print("Cms.read_envdata_to_file() returns " + str(n) + " (expected 0)")
    assert (0 == n)
    _dump_file(outputfile)

    # Check we got the same as we started
    assert (read_text_file(outputfile) == mytext)

    print("\nDo the same but using string-->file mode...")
    print("DATA:", mytext)
    envdatafile = 'cms2bobandcarl1.p7m'
    n = Cms.make_envdata_from_string(envdatafile, mytext, certlist)
    print("Cms.make_envdata_from_string() returns " + str(n) + " (expected 2 = # of recipients)")
    assert (n > 0)
    print("Asn1.type('" + envdatafile + "')-->" + Asn1.type(envdatafile))
    s = Cms.read_envdata_to_string(envdatafile, prikeystr)
    print(s)

    print("\nDo the same but using bytes-->file mode...")
    mydata = "Olá mundo".encode()
    print("DATA:", mydata)
    envdatafile = 'cms2bobandcarl2.p7m'
    n = Cms.make_envdata_from_bytes(envdatafile, mydata, certlist)
    print("Cms.make_envdata_from_string() returns " + str(n) + " (expected 2 = # of recipients)")
    assert (n > 0)
    print("Asn1.type('" + envdatafile + "')-->" + Asn1.type(envdatafile))
    s = Cms.read_envdata_to_string(envdatafile, prikeystr)
    print("Cms.read_envdata_to_string=", s)
    b = Cms.read_envdata_to_bytes(envdatafile, prikeystr)
    print("Cms.read_envdata_to_bytes=", b)

    # clean up
    prikeystr = None


def test_smime():
    print("\nTESTING S/MIME...")
    print("First create an enveloped-data message for Bob and Carl...")
    # Create a file
    mytext = 'This is some sample content.'
    myfile = "mycontent.txt"
    write_text_file(myfile, mytext)
    envdatafile = 'cms2bobandcarl.p7m'
    certlist = "BobRSASignByCarl.cer;CarlRSASelf.cer"
    n = Cms.make_envdata(envdatafile, myfile, certlist)
    print("Cms.make_envdata() returns " + str(n) + " (expected 2 = # of recipients)")
    assert (n > 0)
    print("Asn1.type('" + envdatafile + "')-->" + Asn1.type(envdatafile))
    print("Now wrap in S/MIME headers...")
    smimefile = 'cms2bobandcarl-smime-env.txt'
    n = Smime.wrap(smimefile, envdatafile)
    print("Smime.wrap() returns ", n, " (expected +ve)")
    _dump_file(smimefile)

    print("Query this S/MIME entity for info...")
    query = "content-type"
    r = Smime.query(smimefile, query)
    print("Smime.query('%s')=[%s]" % (query, r))
    query = "smime-type"
    r = Smime.query(smimefile, query)
    print("Smime.query('%s')=[%s]" % (query, r))

    print("Extract the original CMS env-data object in base64")
    extractedfile = 'cms2bobandcarl-extracted.txt'
    n = Smime.extract(extractedfile, smimefile, Smime.Opts.ENCODE_BASE64)
    print("Smime.extract() returns ", n, " (expected +ve)")
    assert n > 0
    _dump_file(extractedfile)
    # Read base64 data into a string then analyze
    s = read_text_file(extractedfile)
    print("Asn1.type('" + extractedfile + "')-->" + Asn1.type(s))


def test_cms_sigdata():
    print("\nTESTING CMS SIG-DATA...")
    print("Create an signed-data message from Alice, using file-->file mode")
    # Create a file
    myfile = "mycontent.txt"
    mytext = 'This is some sample content.'
    write_text_file(myfile, mytext)
    # Alice reads in her private key to a secure "internal" key string
    prikeystr = Rsa.read_private_key('AlicePrivRSASign.p8e', 'password')
    certlist = "AliceRSASignByCarl.cer"
    sigdatafile = 'cms_signedbyalice.p7m'
    n = Cms.make_sigdata(sigdatafile, myfile, certlist, prikeystr)
    print("Cms.make_sigdata() returns " + str(n) + " (expected 0)")
    assert (n == 0)
    print("Asn1.type('" + sigdatafile + "')-->" + Asn1.type(sigdatafile))

    print("\nQuery this CMS object file...")
    fname = sigdatafile
    query = "signatureAlgorithm"
    res = Cms.query_sigdata(sigdatafile, query)
    print("Cms.query_sigdata(" + fname + ", " + query + "):", res)
    query = "CountOfSignerInfos"
    res = Cms.query_sigdata(sigdatafile, query)
    print("Cms.query_sigdata(" + fname + ", " + query + "):", res)

    print("\nRead in the content from the signed-data file...")
    outputfile = "alicesdata.txt"
    n = Cms.read_sigdata_to_file(outputfile, sigdatafile)
    print("Cms.read_sigdata_to_file() returns " + str(n) + " (expected 0)")
    assert (0 == n)
    _dump_file(outputfile)

    print("\nVerify the signature in the sigdata file...")
    isok = Cms.verify_sigdata(sigdatafile)
    print("Cms.verify_sigdata() returns", isok)
    assert isok

    print("\nUse string-->file mode...")
    print("DATA:", mytext)
    sigdatafile1 = 'cms_signedbyalice1.p7m'
    n = Cms.make_sigdata_from_string(sigdatafile1, mytext, certlist, prikeystr)
    print("Cms.make_sigdata_from_string() returns " + str(n) + " (expected 0)")
    assert (n == 0)
    print("Asn1.type('" + sigdatafile1 + "')-->" + Asn1.type(sigdatafile1))

    s = Cms.read_sigdata_to_string(sigdatafile)
    print(s)

    print("signed-data files should be identical...")
    print("SHA1('" + sigdatafile + "')=\t" + Hash.hex_from_file(sigdatafile))
    print("SHA1('" + sigdatafile1 + "')=\t" + Hash.hex_from_file(sigdatafile1))
    assert (Hash.hex_from_file(sigdatafile) == Hash.hex_from_file(sigdatafile1))

    print("\nUse bytes-->file mode...")
    mydata = "Olá mundo".encode()
    print("DATA:", mydata)
    sigdatafile1 = 'cms_signedbyalice2.p7m'
    n = Cms.make_sigdata_from_bytes(sigdatafile1, mydata, certlist, prikeystr)
    print("Cms.make_sigdata_from_bytes() returns " + str(n) + " (expected 0)")
    assert (n == 0)
    print("Asn1.type('" + sigdatafile1 + "')-->" + Asn1.type(sigdatafile1))

    b = Cms.read_sigdata_to_bytes(sigdatafile1)
    print(b)

    print("\nMake a 'detached signature' signed-data object using the message digest of the content...")
    hexdigest = Hash.hex_from_string(mytext, Hash.Alg.SHA256)
    print("SHA256('%s')=%s" % (mytext, hexdigest))
    sigdatafile_det = 'cms_signedbyalice_det.p7m'
    n = Cms.make_detached_sig(
        sigdatafile_det, hexdigest, certlist, prikeystr, sigalg=Cms.SigAlg.RSA_PSS_SHA256)
    print("Cms.make_detached_sig() returns " + str(n) + " (expected 0)")
    assert (n == 0)
    print("Verify the signature in the detached sigdata file against the digest value...")
    print("First try verifying against the eContent (which is missing)...")
    try:
        isok = Cms.verify_sigdata(sigdatafile_det)
    except PKIError as e:
        print("Woops! PKIError:", e)
    print("Now pass the digest we expect...")
    isok = Cms.verify_sigdata(sigdatafile_det, hexdigest=hexdigest)
    print("Cms.verify_sigdata(file,hexdigest) returns", isok)
    assert isok
    print("Query the signature and digest algorithms used in our signed-data object (expecting rsaPSS/sha256)")
    query = "signatureAlgorithm"
    s = Cms.query_sigdata(sigdatafile_det, query)
    print(query + "=[" + s + "]")
    query = "digestAlgorithm"
    s = Cms.query_sigdata(sigdatafile_det, query)
    print(query + "=[" + s + "]")

    print("\nCreate signed-data from a pre-computed signature value...")
    # Example 4.2 from [SMIME-EX]
    # Data to be signed
    datahex = ("54:68:69:73:20:69:73:20:73:6f:6d:65:20:73:61:6d"
               "70:6c:65:20:63:6f:6e:74:65:6e:74:2e")
    data = Cnv.fromhex(datahex)
    print("DATA:", Cnv.tohex(data))
    # Signature value generated by smartcard using rsa-sha1 (our default)
    sighex = ("2F:23:82:D2:F3:09:5F:B8:0C:58:EB:4E:9D:BF:89:9A"
              "81:E5:75:C4:91:3D:D3:D0:D5:7B:B6:D5:FE:94:A1:8A"
              "AC:E3:C4:84:F5:CD:60:4E:27:95:F6:CF:00:86:76:75"
              "3F:2B:F0:E7:D4:02:67:A7:F5:C7:8D:16:04:A5:B3:B5"
              "E7:D9:32:F0:24:EF:E7:20:44:D5:9F:07:C5:53:24:FA"
              "CE:01:1D:0F:17:13:A7:2A:95:9D:2B:E4:03:95:14:0B"
              "E9:39:0D:BA:CE:6E:9C:9E:0C:E8:98:E6:55:13:D4:68"
              "6F:D0:07:D7:A2:B1:62:4C:E3:8F:AF:FD:E0:D5:5D:C7")
    sig = Cnv.fromhex(sighex)
    print("SIG:", Cnv.tohex(sig))
    sigdatafile2 = 'cms_signedbyalice2.p7m'
    n = Cms.make_sigdata_from_sigvalue(sigdatafile2, sig, data, certlist)
    print("Cms.make_sigdata_from_sigvalue() returns " + str(n) + " (expected 0)")
    # Compare resulting file to expected `4.2.bin`
    print("SHA1(outputfile)=", Hash.hex_from_file(sigdatafile2))
    print("SHA1('4.2.bin' )=", Hash.hex_from_file('4.2.bin'))
    assert (Hash.hex_from_file(sigdatafile2) == Hash.hex_from_file('4.2.bin'))


def test_cms_comprdata():
    print("\nTESTING CMS COMPRESSED-DATA...")
    print("Creating an compressed-data object...")
    basefile = "sonnets.txt"
    compfile = 'sonnets.p7z'
    print("INPUT:", basefile, os.path.getsize(basefile), "bytes")
    n = Cms.make_comprdata(compfile, basefile)
    print("Cms.make_comprdata() returns " + str(n) + " (expected 0)")
    assert (n == 0)
    print("COMPR:", compfile, os.path.getsize(compfile), "bytes")
    print("Asn1.type('" + compfile + "')-->" + Asn1.type(compfile))

    print("Reading an compressed-data object...")
    chkfile = "sonnets-unCompr.txt"
    n = Cms.read_comprdata(chkfile, compfile)
    print("Cms.read_comprdata() returns " + str(n) + " (expected +ve)")
    assert (n > 0)
    print("UNCPR:", chkfile, os.path.getsize(chkfile), "bytes")
    # Compare base file to final uncompressed
    print("SHA1(basefile)=", Hash.hex_from_file(basefile))
    print("SHA1(uncmfile)=", Hash.hex_from_file(chkfile))
    assert (Hash.hex_from_file(basefile) == Hash.hex_from_file(chkfile))

    print("Read with no-inflate option...")
    chkfile = "sonnets-noinflate.txt"
    n = Cms.read_comprdata(chkfile, compfile, Cms.ComprDataOpts.NO_INFLATE)
    assert (n > 0)
    print("NOINF:", chkfile, os.path.getsize(chkfile), "bytes")


def test_sig_rsa():
    print("\nTESTING SIG FUNCTIONS USING Rsa...")

    print("Sign the string 'abc' using Alice's private RSA key...")
    keyfile = "AlicePrivRSASign.p8e"
    password = "password"  # !!!
    alg = Sig.Alg.RSA_SHA1

    # Sign data
    data = b"abc"
    sig = Sig.sign_data(data, keyfile, password, alg)
    print("sign_data:  ", sig)

    # Sign the digest value of the data
    digest = Cnv.fromhex("a9993e364706816aba3e25717850c26c9cd0d89d")
    sig1 = Sig.sign_digest(digest, keyfile, password, alg)
    print("sign_digest:", sig1)
    assert (sig1 == sig)

    # Encode the signature differently
    print("Different encodings...")
    sig2 = Sig.sign_data(data, keyfile, password, alg,
                         encoding=Sig.Encoding.BASE64URL)
    print("sign_data:  ", sig2)
    sig3 = Sig.sign_data(data, keyfile, password, alg,
                         encoding=Sig.Encoding.HEX)
    print("sign_data:  ", sig3)

    print("Verify the signature over the data")
    cert = "AliceRSASignByCarl.cer"
    isok = Sig.data_is_verified(sig, data, cert, alg)
    print("Sig.data_is_verified() returns", isok)
    assert (isok)

    print("Use the wrong cert...")
    wrongcert = "BobRSASignByCarl.cer"
    isok = Sig.data_is_verified(sig, data, wrongcert, alg)
    print("Sig.data_is_verified() returns", isok, "(expected False)")
    assert (not isok)

    print("Verify the signature over the message digest value")
    isok = Sig.digest_is_verified(sig, digest, cert, alg)
    print("Sig.digest_is_verified() returns", isok)
    assert (isok)

    print("Sign a file containing 'abc' using Alice's private RSA key...")
    datafile = "abc.txt"
    write_text_file(datafile, 'abc')
    sig = Sig.sign_file(datafile, keyfile, password, alg)
    print("sign_file:  ", sig)
    # Verify it
    isok = Sig.file_is_verified(sig, datafile, cert, alg)
    print("Sig.file_is_verified() returns", isok)
    assert (isok)


def test_sig_ecc():
    print("\nTESTING SIG FUNCTIONS USING Ecc...")

    # Ref: [RFC6979] "Deterministic Usage of the DSA and ECDSA"
    # A.2.3.  ECDSA, 192 Bits (Prime Field)

    # Read in private key using (hex,curvename) form
    keyhex = "6FAB034934E4C0FC9AE67F5B5659A9D7D1FEFD187EE09FD4"
    curvename = Ecc.CurveName.P_192
    print("KEYHEX:", keyhex)
    print("CURVE:", curvename)
    keystr = Ecc.read_key_by_curve(keyhex, curvename)
    print("NBITS=", Ecc.query_key(keystr, "keyBits"))

    # Sign data
    alg = Sig.Alg.ECDSA_SHA1
    data = b"test"
    sig = Sig.sign_data(data, keystr, "", alg, opts=Sig.Opts.DETERMINISTIC, encoding=Sig.Encoding.HEX)
    print("SIG:", sig)

    print("Verify the signature over the data...")
    # Derive the EC public key from the private key
    pubkeystr = Ecc.publickey_from_private(keystr)
    # And use it to verify the signature
    isok = Sig.data_is_verified(sig, data, pubkeystr, alg)
    print("Sig.data_is_verified() returns", isok)
    assert (isok)


def test_x509_ecc():
    print("\nTESTING X509 CERT FUNCTIONS USING Ecc...")  # New in v11.3

    # Use an EC key we made earlier
    cakeyfile = 'ecprivkey.p8'  # in pkiPythonTestFiles.zip
    password = 'password'
    cacert = 'myca_Ecc.cer'
    dn = "O=My Company;OU=My Org;E=me@org.com;L=Perth;ST=WA;C=AU;CN=Test Example"
    extns = "serialNumber=#x00F3ED4B1754C18AA5;notBefore=2017-09-19T08:09:06Z;notAfter=2027-09-17T08:09:06Z"

    # Make a new self-signed certificate...
    # (just for testing purposes we use the deterministic method for ECDSA, so we always get the same result)
    print("About to create new certificate:", cacert)
    r = X509.make_cert_self(cacert, cakeyfile, password, 0, 0, dn, extns, sigalg=X509.SigAlg.ECDSA_SHA256,
                            opts=X509.Opts.VERSION1 | X509.Opts.DETERMINISTIC)
    assert (0 == r)

    # Query this new cert
    certname = cacert
    print("serialNumber:", X509.query_cert(certname, "serialNumber"))
    print("issuerName:", X509.query_cert(certname, "issuerName"))
    print("signatureAlgorithm:", X509.query_cert(certname, "signatureAlgorithm"))
    print("hashAlgorithm:", X509.query_cert(certname, "hashAlgorithm"))
    print("subjectPublicKeyAlgorithm:", X509.query_cert(certname, "subjectPublicKeyAlgorithm"))

    # Dump its details (new fn in v11.3)
    dump = X509.text_dump_tostring(certname)
    print("FILE:", certname)
    print(dump)

    # Verify this new certificate using itself
    isok = X509.cert_is_verified(cacert, cacert)
    print("X509.cert_is_verified({0}, {1}) returns {2}".format(cacert, cacert, isok))
    assert (isok)

    # Read in the EC public key value from the X.509 certificate (new in v11.3)
    # (just to show we can!)
    pubkey = Ecc.read_public_key(cacert)
    assert (len(pubkey) > 0)
    print("Public key size:", Ecc.query_key(pubkey, "keyBits"), "bits")

    # Generate a new EC key pair for an end user
    userprikeyfile = 'myuser_prikey.p8'
    userpubkeyfile = 'myuser_pubkey.pub'
    r = Ecc.make_keys(userpubkeyfile, userprikeyfile, Ecc.CurveName.P_224, "password")
    print("Created new user key pair:", userprikeyfile, "&", userpubkeyfile)
    assert (0 == r)

    # Create a new end-user certificate using EC key we just made
    usercert = 'myuser_Ecc.cer'
    dn = "CN=Olá mundo;OU=Using ECC_P224"
    print("About to create new certificate:", usercert)
    r = X509.make_cert(usercert, cacert, userpubkeyfile, cakeyfile, password, 0x224, 5, dn,
                       sigalg=X509.SigAlg.ECDSA_SHA224, opts=X509.Opts.UTF8)
    assert (0 == r)

    # Query this new cert
    certname = usercert
    print("serialNumber:", X509.query_cert(certname, "serialNumber"))
    print("issuerName:", X509.query_cert(certname, "issuerName"))
    # User name is encoded in UTF-8: default is to display in hex
    print("subjectName:", X509.query_cert(certname, "subjectName"))

    # Display as latin-1 string properly in IDE
    # -- No longer an issue with Python 3!!
    # print("subjectName:", X509.query_cert(certname, "subjectName", X509.Opts.LATIN1).decode('iso-8859-1'))

    print("signatureAlgorithm:", X509.query_cert(certname, "signatureAlgorithm"))
    print("hashAlgorithm:", X509.query_cert(certname, "hashAlgorithm"))
    print("subjectPublicKeyAlgorithm:", X509.query_cert(certname, "subjectPublicKeyAlgorithm"))

    # Verify this new certificate using CA's cert
    isok = X509.cert_is_verified(usercert, cacert)
    print("X509.cert_is_verified({0}, {1}) returns {2}".format(usercert, cacert, isok))
    assert (isok)

    # Verify the path
    certlist = usercert + ";" + cacert
    isok = X509.cert_path_is_valid(certlist)
    print("X509.cert_path_is_valid({0}) returns {1}".format(certlist, isok))
    assert (isok)


def test_asn1_dumptostring():
    print("\nTESTING ASN.1 TEXT DUMP TO STRING...")  # New in v11.3
    fname = r"C:\!Data\Crypto\X509\x509cat.Asn1.dat"
    s = Asn1.text_dump_tostring(fname)
    # File is large! Just dump the first part
    print(s[:378])


def test_compress():
    print("\nTEST ZLIB COMPRESSION....")

    message = b"hello, hello, hello. This is a 'hello world' message for the world, repeat, for the world."
    print("MSG:", message)
    comprdata = Compr.compress(message)
    print("Compressed = (0x)" + Cnv.tohex(comprdata))
    print("Compressed %d bytes to %d" % (len(message), len(comprdata)))
    # Now uncompresss (inflate)
    uncomprdata = Compr.uncompress(comprdata)
    print("Uncompressed = '" + str(uncomprdata) + "'")
    assert (uncomprdata == message)


def test_aead():
    print("\nTEST AES-GCM AUTHENTICATED ENCRYPTION....")

    # GCM Test Case #03 (AES-128)
    key = Cnv.fromhex("feffe9928665731c6d6a8f9467308308")
    iv = Cnv.fromhex("cafebabefacedbaddecaf888")
    pt = Cnv.fromhex(
        "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255")
    okhex = "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f59854d5c2af327cd64a62cf35abd2ba6fab4"
    print("KY =", Cnv.tohex(key))
    print("IV =", Cnv.tohex(iv))
    print("PT =", Cnv.tohex(pt))
    # Do the business
    ct = Cipher.encrypt_aead(pt, key, iv, Cipher.AeadAlg.AES_128_GCM)
    print("CT =", Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == Cnv.tohex(ct).lower())

    # Decrypt, passing IV as an argument
    dt = Cipher.decrypt_aead(ct, key, iv, Cipher.AeadAlg.AES_128_GCM)
    print("DT =", Cnv.tohex(dt))
    assert (Cnv.tohex(pt) == Cnv.tohex(dt))

    print("Repeat but prepend IV to output..")
    ct = Cipher.encrypt_aead(pt, key, iv, Cipher.AeadAlg.AES_128_GCM, opts=Cipher.Opts.PREFIXIV)
    print("IV|CT =", Cnv.tohex(ct))
    # Decrypt, IV is prepended to ciphertext
    dt = Cipher.decrypt_aead(ct, key, None, Cipher.AeadAlg.AES_128_GCM, opts=Cipher.Opts.PREFIXIV)
    print("DT =", Cnv.tohex(dt))
    assert (Cnv.tohex(pt) == Cnv.tohex(dt))


def test_aead_chapoly():
    print("\nTEST AEAD CHACHA20POLY1305....")
    print("RFC8439 ChaCha20_Poly1305 Sunscreen test with AAD")
    key = Cnv.fromhex("808182838485868788898A8B8C8D8E8F909192939495969798999A9B9C9D9E9F")
    iv = Cnv.fromhex("070000004041424344454647")
    aad = Cnv.fromhex("50515253C0C1C2C3C4C5C6C7")
    pt = Cnv.fromhex(
        "4C616469657320616E642047656E746C656D656E206F662074686520636C617373206F66202739393A204966204920636F756C64206F6666657220796F75206F6E6C79206F6E652074697020666F7220746865206675747572652C2073756E73637265656E20776F756C642062652069742E")
    okhex = "d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b61161ae10b594f09e26a7e902ecbd0600691"
    print("KY =", Cnv.tohex(key))
    print("IV =", Cnv.tohex(iv))
    print("AD =", Cnv.tohex(aad))
    print("PT =", Cnv.tohex(pt))
    # Do the business
    ct = Cipher.encrypt_aead(pt, key, iv, Cipher.AeadAlg.CHACHA20_POLY1305, aad=aad)
    print("CT =", Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == Cnv.tohex(ct).lower())
    dt = Cipher.decrypt_aead(ct, key, iv, Cipher.AeadAlg.CHACHA20_POLY1305, aad=aad)
    print("DT =", Cnv.tohex(dt))
    print(f"DT ='{dt.decode()}'")
    assert (Cnv.tohex(pt) == Cnv.tohex(dt))
    # Again but prefix the IV to the ciphertext
    print(f"Prefix the IV ({Cnv.tohex(iv)}) to the CT...")
    ct = Cipher.encrypt_aead(pt, key, iv, Cipher.AeadAlg.CHACHA20_POLY1305, aad=aad, opts=Cipher.Opts.PREFIXIV)
    print("CT =", Cnv.tohex(ct))
    dt = Cipher.decrypt_aead(ct, key, iv, Cipher.AeadAlg.CHACHA20_POLY1305, aad=aad, opts=Cipher.Opts.PREFIXIV)
    print("DT =", Cnv.tohex(dt))
    assert (Cnv.tohex(pt) == Cnv.tohex(dt))


def test_readcertstring():
    print("\nTEST READ CERT STRING FROM P7CHAIN AND Pfx....")

    # Input is a P7 chain file in PEM format
    # bob.p7b (contains 2 X.509 certs: BobRSA and CarlRSA)
    strp7 = """-----BEGIN PKCS7-----
        MIIERQYJKoZIhvcNAQcCoIIENjCCBDICAQExADALBgkqhkiG9w0BBwGgggQaMIICJzCCAZCgAwIB
        AgIQRjRrx4AAVrwR024uzV1x0DANBgkqhkiG9w0BAQUFADASMRAwDgYDVQQDEwdDYXJsUlNBMB4X
        DTk5MDkxOTAxMDkwMloXDTM5MTIzMTIzNTk1OVowETEPMA0GA1UEAxMGQm9iUlNBMIGfMA0GCSqG
        SIb3DQEBAQUAA4GNADCBiQKBgQCp4WeYPznVX/Kgk0FepnmJhcg1XZqRW/sdAdoZcCYXD72lItA1
        hW16mGYUQVzPt7cIOwnJkbgZaTdt+WUee9mpMySjfzu7r0YBhjY0MssHA1lS/IWLMQS4zBgIFEjm
        Txz7XWDE4FwfU9N/U9hpAfEF+Hpw0b6Dxl84zxwsqmqn6wIDAQABo38wfTAMBgNVHRMBAf8EAjAA
        MA4GA1UdDwEB/wQEAwIFIDAfBgNVHSMEGDAWgBTp4JAnrHggeprTTPJCN04irp44uzAdBgNVHQ4E
        FgQU6PS4Z9izlqQq8xGqKdOVWoYWtCQwHQYDVR0RBBYwFIESQm9iUlNBQGV4YW1wbGUuY29tMA0G
        CSqGSIb3DQEBBQUAA4GBAHuOZsXxED8QIEyIcat7QGshM/pKld6dDltrlCEFwPLhfirNnJOIh/uL
        t359QWHh5NZt+eIEVWFFvGQnRMChvVl52R1kPCHWRbBdaDOS6qzxV+WBfZjmNZGjOd539OgcOync
        f1EHl/M28FAK3Zvetl44ESv7V+qJba3JiNiPzyvTMIIB6zCCAVSgAwIBAgIQRjRrx4AAVrwR024u
        n/JQIDANBgkqhkiG9w0BAQUFADASMRAwDgYDVQQDEwdDYXJsUlNBMB4XDTk5MDgxODA3MDAwMFoX
        DTM5MTIzMTIzNTk1OVowEjEQMA4GA1UEAxMHQ2FybFJTQTCBnzANBgkqhkiG9w0BAQEFAAOBjQAw
        gYkCgYEA5Ev/GLgkV/R3/25ze5NxXLwzGpKSciPYQUbQzRE6BLOOr4KdvVEeF3rydiwrhjmnvdeN
        GlPs5ADV6OyiNrHt4lDiMgmKP5+ZJY+4Tqu5fdWWZdoWoMW+Dq5EW+9e9Kcpy4LdrETpqpOUKQ74
        GNbIV17ydsTyEWA4uRs8HZfJavECAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8E
        BAMCAYYwHQYDVR0OBBYEFOngkCeseCB6mtNM8kI3TiKunji7MA0GCSqGSIb3DQEBBQUAA4GBALee
        1ATT7Snk/4mJFS5M2wzwSA8yYe7EBOwSXS3/D2RZfgrD7Rj941ZAN6cHtfA4EmFQ7e/dP+MLuGGl
        pJs85p6cVJq2ldbabDu1LUU1nUkBdvq5uTH5+WsSU6D1FGCbfco+8lNrsDdvreZ019v6WuoUQWNd
        zb7IDsHaao1TNBgCMQA=
        -----END PKCS7-----"""
    # Get count of certs in P7 chain
    ncerts = X509.get_cert_count_from_p7(strp7)
    print("ncerts in P7 chain =", ncerts)
    for i in range(1, ncerts + 1):
        certstr = X509.read_cert_string_from_p7chain(strp7, i)
        print("CER:", certstr[:80], "...", certstr[-10:])
        subjectname = X509.query_cert(certstr, "subjectName")
        print("subjectName:", subjectname)

    # Input is a PFX file in PEM format
    # bob.pfx (password="password")
    strpfx = """-----BEGIN PKCS12-----
        MIIGhAIBAzCCBkoGCSqGSIb3DQEHAaCCBjsEggY3MIIGMzCCAv8GCSqGSIb3DQEHBqCCAvAwggLsAgEAMIIC5QYJKoZIhvcNAQcBMBwGCiqGSIb3DQEMAQYwDgQIawU
        AVTFvAiECAggAgIICuNwEuFcRnZamZyMyIn+vH+wC5BVUtZAWNrlIqToezF7cYqt/18+HXB/46nllz+qUD3Dv9rS78MnPeAM47afFRTricHsiOpE+2eXf32lxduoF5+
        CLS3S7TAhRUMp2Fh18LlukzK9lY67BGfU9Y3yCukTmwVXqe49dkj8y9JjVJhXnoc2c7eOk3o5RjXHFsAMHwirqdsESHstrDZYLMVGw5HnAamY7zQd8WUpIweAFaEDLJ
        fyzqY1/LTL/txvZ9VQ/B/36HKyEpoIvuH6iOCBkebpJwWSkkffuVFbUfMLguMztL/sf+jE2NiuljSBJ9pTNsZziZWERb6CxZH0a2xkkBTciXM5Dl5efWL0GmBg+aJSI
        yh+Gw5W8Q7gmnH6H9myszvW9uYv/epwCbIpHd0dRHPbL3fR4KGhFexq24tAG86tDqPKb6H6n0lSA+Oq46SwZ00xIFpVcFaO/8yVqf6+JRDGoZ55aAZF6OCi7R1GvI+6
        pzz37pvP7SWfqVSuXCTNQq9uKw97SH5YftQ9hkELQ4vHCjFh4UJSBUCZgDtqR1uB/+44H5UpP8KvbETaOFJszMxsqXBMqc1uEODSNg+EHEx+yg7Bx1CcNrm+6rtThC4
        9+ow18HDMxbn3lAw1ooblANvSzR4YTt68N/4dtwROOdXjwKzyg03qWK2sJaiH5LzbB5MMmrdAChb9dLoRKBN2LREob7KRKEs6v51IW1yq4UCwSmpP+RbchZwIoKVXx/
        MYKjVqzGfZAgBRpXEq/KH/8R+ttFPKdab2GAEjd7hIOmetp5einQmK4C7JYE6Uyabf1IImtVhBw2dGU3GiM2zSIGqCx3bmYETZheMTAV9MMVUYe8gQeEpbXM4GAnwX0
        wpS0aYapzGeA/62X2nFh21eRHVzUcf0miXVvyOy6a1vj6O6N5F1jVaCV3jCCAywGCSqGSIb3DQEHAaCCAx0EggMZMIIDFTCCAxEGCyqGSIb3DQEMCgECoIICpjCCAqI
        wHAYKKoZIhvcNAQwBAzAOBAjw/dx4SlLcWwICCAAEggKALm91I8gYuPpRTCSn5pN4OQBLbI6jSW+9FGeNYvOy/+Pt3Oq0i15ZXZZez7dP8rdb0tmTCSZwVPIwtJRKxY
        UNaTppUTWZhXhnmeTMtSZpFuKmo6UhW8lGUcg45sO5UKUtdH0/UgewaSUfV4L06vp4j7Fugwbp666seJJ/9vQwMAxoqj0blxNNmASAcW7yj/lA2/p4KuGlnGkv4MSW5
        ViH7T24VeFXTzyFFR7UR1Nw9Blr5jdr7b2rZSdTj0GeHZ/L3FksFWJocl8PEEL4ZdVscbvO+l7vtbeBz0y9TDr/HUwt2tfqXgjckVVoJhmsczJXrG5Ai+brKnGQ7R5u
        IpIsqd9O6EpG68VMMGA5iSKsLYtibieqom8mRO00sFiQharxONEdveY+3O98nG6xzHlaBdNbxVo38Y+4LK6Gc81dUWYwss3ajdiJWe0+TYQjMPF72eWctcQAoTxITpd
        /j6rD7EmvLVyPIR46L4w6Gb/uz5G1T1UiLoh9luM1nRKKICyo2XllZDNO0msaub7DH1xzJzEy2OT9cwChqYfKKeWEE2BWL699fmq5RMCbIQVtE2bJDP8obu9j6HLskC
        iZcJm6nC7IKS1pQ2BA/JJVKxC8ADuLOAOdicWquDd8MWL5a9HpXd5TtUlfiRecTw8IRozTLaoDVlhaYNGPzwkjL9zZ+Up5Uy6HHXMDb0aD0fgvMqdAspB1+Xlt2RgP6
        CnEH2hwQqGFoA8TtijeS+DtdMy8BxJ7g1fiEH0+4UISl1vymjPI1MJCI1VlFLvpjZvKHluwjgp1SHk3tFRJLJ8a/eApvmscKXSlxcYz+5Bv8dxPGdhO/KOLQS7XZ4a8
        VSg977WS1jFYMCMGCSqGSIb3DQEJFTEWBBRj8EbS3XBC5R/cJqUR73yB6mItizAxBgkqhkiG9w0BCRQxJB4iAEIAbwBiACcAcwAgAGYAcgBpAGUAbgBkAGwAeQAgAEk
        ARDAxMCEwCQYFKw4DAhoFAAQUaHSMUJ415FfKGv3cZpwloKDmqgYECAreM3EkHVjCAgIIAA==
        -----END PKCS12-----"""
    certstr = X509.read_cert_string_from_pfx(strpfx, "password")
    print("CER:", certstr[:80], "...", certstr[-10:])
    subjectname = X509.query_cert(certstr, "subjectName")
    print("subjectName:", subjectname)


# NEW IN [v12.3]

def test_cipher_prefix():
    print("\nENCRYPT WITH PREFIXED IV xmlenc#aes128-cbc...")
    plain = "<encryptme>hello world</encryptme>"
    key = Cnv.fromhex("6162636465666768696A6B6C6D6E6F70")
    iv = Rng.bytestring(Cipher.blockbytes(Cipher.Alg.AES128))
    print("PT='", plain, "'", sep='')
    pt = plain.encode()
    print("HEX(PT)=", Cnv.tohex(pt), sep='')
    print("KEY=", Cnv.tohex(key), sep='')
    print("IV=", Cnv.tohex(iv), sep='')
    # Encrypt and prepend IV before ciphertext
    ct = Cipher.encrypt(pt, key, iv, "aes128/cbc", opts=Cipher.Opts.PREFIXIV)
    print("IV|CT=", Cnv.tohex(ct), sep='')
    # Encode in base64
    ciphervalue = Cnv.tobase64(ct)
    # Output in XML (NB will be different each time)
    print("<CipherValue>{0}</CipherValue>".format(ciphervalue))

    # ---------------
    # PART 2 - decrypt
    print("DECRYPTING...")
    # Decode from base64
    ct = Cnv.frombase64(ciphervalue)
    print("IV|CT=", Cnv.tohex(ct), sep='')
    # Decrypt. Note that IV is not specified when decrypting with a prefixed IV
    dt = Cipher.decrypt(ct, key, None, "aes128/cbc", opts=Cipher.Opts.PREFIXIV)
    # Display plaintext
    print("DT=", Cnv.tohex(dt), sep='')
    print("DT='", dt.decode(), "'", sep='')
    assert (Cnv.tohex(pt) == Cnv.tohex(dt))


def test_x509_makecert_emptydn():
    print("\nMAKE CERT WITH EMPTY DN:")
    certname = "AliceRSA-emptyDN.cer"
    issuercert = "CarlRSASelf.cer"
    prikeyfile = "CarlPrivRSASign.p8e"
    password = "password"
    subjectpubkeyfile = "AlicePubRsa.pub"
    dn = "$"  # special flag for empty DN
    extns = "iPAddress=192.168.15.1"  # at least one field for subject alt name is required
    keyusage = X509.KeyUsageFlags.DIGITALSIGNATURE | X509.KeyUsageFlags.NONREPUDIATION

    # Create a new certificate for Alice signed by Carl valid for 2 years signed using RSA-SHA-256
    # Subject's distinguished name will be empty, Subject alternative name will be automatically marked CRITICAL (denoted "[!]" in dump)
    r = X509.make_cert(certname, issuercert, subjectpubkeyfile, prikeyfile, password, 0x1001, 2, dn, extns=extns,
                       sigalg=X509.SigAlg.RSA_SHA256, keyusage=keyusage)
    assert (0 == r)
    print("Created new X509 file '{0}'".format(certname))
    _dump_and_print_x509(certname)


def test_x509_certrequest_emptydn_extkeyusage():
    print("\nMAKE CERTIFICATE SIGNING REQUEST WITH EMPTY DN AND EXTENDED KEY USAGE:")
    csrfile = "req_emptydn_extkeyusage.p10"
    subjectprikeyfile = "AlicePrivRSASign.p8e"
    password = "password"
    dn = "$"  # special flag for empty DN
    # Use extensions parameter to add alt subject name and extended key usage flags
    extns = "iPAddress=192.168.15.1;extKeyUsage=serverAuth,clientAuth,emailProtection,critical;"

    # Create a CSR for Alice
    # Subject's distinguished name is empty, extKeyUsage is marked CRITICAL (denoted "[!]" in dump)
    r = X509.cert_request(csrfile, subjectprikeyfile, password, dn, extns=extns, sigalg=X509.SigAlg.RSA_SHA256)
    assert (0 == r)
    print("Created certificate request '{0}'".format(csrfile))
    _dump_and_print_x509(csrfile)

    certfile = "certfromcsr_emptydn_extkeyusage.cer"
    issuercert = "CarlRSASelf.cer"
    issuerprikeyfile = "CarlPrivRSASign.p8e"
    issuerpassword = "password"
    # Now use this PKCS#10 CSR to create an end-user X.509 certificate for Alice signed by Carl valid for 4 years
    # Pass the csrfile as the subject public key file argument and leave the DN argument empty as a flag to use a CSR instead
    r = X509.make_cert(certfile, issuercert, csrfile, issuerprikeyfile, issuerpassword, 0x10b, 4, "",
                       sigalg=X509.SigAlg.RSA_SHA256)
    assert (0 == r)
    print("Created end-user X.509 certificate '{0}'".format(certfile))
    _dump_and_print_x509(certfile)
    # Query the new certificate
    query = "subjectName"  # empty ''
    s = X509.query_cert(certfile, query)
    print("Query {0}='{1}'".format(query, s))
    query = "subjectAltName"
    s = X509.query_cert(certfile, query)
    print("Query {0}='{1}'".format(query, s))
    query = "extKeyUsageString"
    s = X509.query_cert(certfile, query)
    print("Query {0}='{1}'".format(query, s))


def test_read_x509_from_pfx_3des():
    print("\nREAD IN CERT AS A STRING FROM PFX FILE USING 3DES ENCRYPTION...")
    # PFX file from draft-dkg-lamps-samples-02 with cert encrypted using "stronger" 3DES
    # Ref: IETF LAMPS WG https:#gitlab.com/dkg/lamps-samples
    pfxfile = "bob-lamps.p12"
    password = 'bob'
    print("FILE:", pfxfile)
    certstr = X509.read_cert_string_from_pfx(pfxfile, password)
    assert (len(certstr) > 0)
    print(certstr[:30], "...", certstr[-30:])
    print("subjectName:", X509.query_cert(certstr, "subjectName"))
    print("Asn1.type=", Asn1.type(certstr))


def test_pfx_makefile_3des():
    print("\nCREATE A NEW PFX FILE USING 3DES TO ENCRYPT THE CERT:")
    pfxfile = "bob-3des.pfx"
    prikeyfile = "BobPrivRSAEncrypt.p8e"
    certfile = "BobRSASignByCarl.cer"
    password = "password"
    # Use StrongCert option to encrypt cert using "stronger" 3DES instead of weak default 40-bit RC2.
    r = Pfx.make_file(pfxfile, certfile, prikeyfile, password, "Old Bob", Pfx.Opts.STRONG_CERT)
    assert (0 == r)
    print("Created PKCS#12 key store file '{0}'".format(pfxfile))
    # Now dump the ASN.1
    # Note that certificate (in encryptedData) is encrypted with "pbeWithSHAAnd3-KeyTripleDES-CBC"
    # (see line 275 (approx) of output)
    _dump_and_print_asn1(pfxfile)


def test_rng_guid():
    print("\nTEST RANDOM GUID STRINGS...")
    for x in range(0, 5):
        guid = Rng.guid()
        print(guid)


def test_sig_signdata_ed25519():
    print("\nSIGN DATA USING Ed25519...")
    # Ref: [RFC8032] https://tools.ietf.org/html/rfc8032#section-7.1
    # -----TEST SHA(abc)
    # Read in private key from hex (NB need explicitly to identify as a private key)
    prikey = Ecc.read_key_by_curve("833fe62409237b9d62ec77587520911e9a759cec1d19755b7da901b96dca3d42",
                                   Ecc.CurveName.ED25519, Ecc.KeyType.PRIVATE_KEY)
    print(f"Private key has {Ecc.query_key(prikey, 'keyBits')} bits")
    print(f"ALGORITHM: {Ecc.query_key(prikey, 'curveName')}")
    # Message is the 64-byte SHA-512 hash of "abc"
    message = Cnv.fromhex(
        "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f")
    # Compute signature value in hex
    sig = Sig.sign_data(message, prikey, "", Sig.Alg.ED25519, encoding=Sig.Encoding.HEX)
    print(f"SIGNATURE:\n{sig}")
    # Check against known correct result
    sigok = "dc2a4459e7369633a52b1bf277839a00201009a3efbf3ecb69bea2186c26b58909351fc9ac90b3ecfdfbc7c66431e0303dca179c138ac17ad9bef1177331a704"
    assert (sig == sigok)

    # Now verify using public key
    pubkey = Ecc.read_key_by_curve("ec172b93ad5e563bf4932c70e1245034c35467ef2efd4d64ebf819683467e2bf",
                                   Ecc.CurveName.ED25519, Ecc.KeyType.PUBLIC_KEY)
    print(f"Public key has {Ecc.query_key(pubkey, 'keyBits')} bits")
    ok = Sig.data_is_verified(sig, message, pubkey, Sig.Alg.ED25519)
    print(f"Sig.data_is_verified() returns {ok}")
    assert (ok)


def test_sig_signdata_ed448():
    print("\nSIGN DATA USING Ed448...")
    # Ref: [RFC8032] https://tools.ietf.org/html/rfc8032
    # -----Blank
    # Read in private key from hex (NB need explicitly to identify as a private key)
    prikey = Ecc.read_key_by_curve(
        "6c82a562cb808d10d632be89c8513ebf 6c929f34ddfa8c9f63c9960ef6e348a3 528c8a3fcc2f044e39a3fc5b94492f8f 032e7549a20098f95b",
        Ecc.CurveName.ED448, Ecc.KeyType.PRIVATE_KEY)
    print(f"Private key has {Ecc.query_key(prikey, 'keyBits')} bits")
    print(f"ALGORITHM: {Ecc.query_key(prikey, 'curveName')}")
    # Message is the empty string
    message = Cnv.fromhex("")
    # Compute signature value in hex
    sig = Sig.sign_data(message, prikey, "", Sig.Alg.ED448, encoding=Sig.Encoding.HEX)
    print(f"SIGNATURE:\n{sig}")
    # Check against known correct result
    sigok = "533a37f6bbe457251f023c0d88f976ae2dfb504a843e34d2074fd823d41a591f2b233f034f628281f2fd7a22ddd47d7828c59bd0a21bfd3980ff0d2028d4b18a9df63e006c5d1c2d345b925d8dc00b4104852db99ac5c7cdda8530a113a0f4dbb61149f05a7363268c71d95808ff2e652600"
    assert (sig == sigok)

    # Now verify using public key
    pubkey = Ecc.read_key_by_curve(
        "5fd7449b59b461fd2ce787ec616ad46a 1da1342485a70e1f8a0ea75d80e96778 edf124769b46c7061bd6783df1e50f6c d1fa1abeafe8256180",
        Ecc.CurveName.ED448, Ecc.KeyType.PUBLIC_KEY)
    print(f"Public key has {Ecc.query_key(pubkey, 'keyBits')} bits")
    ok = Sig.data_is_verified(sig, message, pubkey, Sig.Alg.ED448)
    print(f"Sig.data_is_verified() returns {ok}")
    assert (ok)


def test_cms_makesigdata_ed25519():
    print("\nCREATE A CMS SIGNED-DATA OBJECT USING Ed25519...")
    outfile = "SignedData_Ed25519.p7m"
    infile = "excontent.txt"
    certfile = "Ed25519-ietf-selfsigned.cer"  # Self-signed cert created using private Ed25519 key in [RFC8410]
    prikeyfile = "edwards-ietf-ex.p8"  # No password, from [RFC8410]

    # Read in private key to internal key string (no password)
    prikeystr = Ecc.read_private_key(prikeyfile, "")
    print(prikeystr)
    # Create the signed-data object using Ed25519 with signed attributes incl Algorithm Protection
    opts = Cms.SigDataOpts.INCLUDE_ATTRS or Cms.SigDataOpts.ADD_ALGPROTECT
    r = Cms.make_sigdata(outfile, infile, certfile, prikeystr, Cms.SigAlg.ED25519, opts=opts)
    assert 0 == r
    print(f"Created file '{outfile}'")
    # Show ASN.1 dump of file
    print(f"SIGNED-DATA:\n{Asn1.text_dump_tostring(outfile)}")
    # Query the signed-data object
    query = "digestAlgorithm"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")
    query = "signatureAlgorithm"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")
    query = "HASsignedAttributes"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")
    query = "DigestOfSignedAttrs"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")

    # Verify the signed-data
    r = Cms.verify_sigdata(outfile)
    print(f"Cms.verify_sigdata returns {r} (expecting True)")
    assert r
    # Read the signed-data content
    s = Cms.read_sigdata_to_string(outfile)
    print(f"signed-data content='{s}'")
    assert len(s) > 0


def test_cms_makesigdata_ed448():
    print("\nCREATE A CMS SIGNED-DATA OBJECT USING Ed448...")
    outfile = "SignedData_Ed448.p7m"
    infile = "excontent.txt"
    certfile = "Ed448-selfsigned.cer"  # Self-signed cert using Ed448
    prikeyfile = "edkey448.p8"  # No password

    # Read in private key to internal key string (no password)
    prikeystr = Ecc.read_private_key(prikeyfile, "")
    print(prikeystr)
    # Create the signed-data object using EdDSA with signed attributes incl Algorithm Protection
    opts = Cms.SigDataOpts.INCLUDE_ATTRS | Cms.SigDataOpts.ADD_ALGPROTECT
    r = Cms.make_sigdata(outfile, infile, certfile, prikeystr, Cms.SigAlg.ED448, opts=opts)
    assert 0 == r
    print(f"Created file '{outfile}'")
    # Show ASN.1 dump of file
    print(f"SIGNED-DATA:\n{Asn1.text_dump_tostring(outfile)}")
    # Query the signed-data object
    query = "digestAlgorithm"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")
    query = "signatureAlgorithm"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")
    query = "HASsignedAttributes"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")
    query = "HASalgorithmProtection"
    s = Cms.query_sigdata(outfile, query)
    print(f"Cms.query_sigdata({query})={s}")

    # Verify the signed-data
    r = Cms.verify_sigdata(outfile)
    print(f"Cms.verify_sigdata returns {r} (expecting True)")
    assert r
    # Read the signed-data content
    s = Cms.read_sigdata_to_string(outfile)
    print(f"signed-data content='{s}'")
    assert len(s) > 0


def test_x509_makecertself_25519():
    print("\nCREATE A SELF-SIGNED X.509 CERTIFICATE USING Ed25519...")
    # Ref: [RFC8410] https://tools.ietf.org/html/rfc8410
    # 1. Create a new self-*signed* certificate using the Ed25519 key in RFC8410
    certname = "ietf-Ed25519-self.cer"
    prikeyfile = "edwards-ietf.p8"  # No password
    dn = "CN=IETF Test Demo"
    extns = "notBefore=2016-01-01;notAfter=2040-12-31"
    keyusage = X509.KeyUsageFlags.DIGITALSIGNATURE | X509.KeyUsageFlags.KEYCERTSIGN | X509.KeyUsageFlags.CRLSIGN
    r = X509.make_cert_self(certname, prikeyfile, "", 0x0ED25519, 0, dn, extns, keyusage, X509.SigAlg.ED25519,
                            X509.Opts.UTF8)
    print(f"X509.make_cert_self returns {r} (expected 0)")
    assert 0 == r
    print(f"FILE: {certname}")
    print(X509.text_dump_tostring(certname))
    # Do a query on the cert
    query = "signatureAlgorithm"
    s = X509.query_cert(certname, query)
    print(f"X509.query_sigdata({query})={s}")
    assert len(s) > 0

    # 2. Now create a self-*issued* cert using Ed25519 to sign an X25519 public key
    # [RFC8410] 10.2. Example X25519 Certificate
    # NB This is self-*issued* in that the public key is for an X25519 key intended for ECDH,
    # but it is signed using an Ed25519 signature with a key also belonging to ones self.

    # Read in X25519 public key from its hex value
    # NB we *must* specify that it's a public key
    pubkeystr = Ecc.read_key_by_curve("8520F0098930A754748B7DDCB43EF75A0DBF3A0D26381AF4EBA4A98EAA9B4E6A",
                                      Ecc.CurveName.X25519, Ecc.KeyType.PUBLIC_KEY)
    assert len(pubkeystr) > 0
    # Set cert parameters to closely duplicate the cert given in RFC8410 (almost!)
    dn = "CN=IETF Test Demo"
    extns = "notBefore=2016-08-01T12:19:24;notAfter=2040-12-31T23:59:59;keyUsage=noncritical;serialNumber=#x5601474A2A8DC330;" + \
            "subjectKeyIdentifier=9B1F5EEDED043385E4F7BC623C5975B90BC8BB3B"
    keyusage = X509.KeyUsageFlags.KEYAGREEMENT
    issuercert = certname  # Use the self-signed cert we made above to issue this new cert
    certname = "ietf-X25519-self-issued.cer"
    r = X509.make_cert(certname, issuercert, pubkeystr, prikeyfile, "", 0, 0, dn, extns, keyusage, X509.SigAlg.ED25519,
                       X509.Opts.UTF8)
    assert 0 == r
    print(f"FILE: {certname}")
    # Dump cert details
    print(X509.text_dump_tostring(certname))
    # Query the public key algorithm
    query = "subjectPublicKeyAlgorithm"
    s = X509.query_cert(certname, query)
    print(f"X509.query_sigdata({query})={s}")
    assert len(s) > 0

    # Verify that this cert was signed by the one above
    f = X509.cert_is_verified(certname, issuercert)
    print(f"X509.cert_is_verified returns {f}")
    assert f, "cert verification failed"


def test_cms_pseudo():
    print("\nCREATE A SIGNED-DATA CMS OBJECT USING 'PSEUDO' PLACEHOLDER...")
    # NB signature will be different each time because signingTime is different every time
    pseudofile = "BasicSignByAlice_pseudo.p7m"
    opts = Cms.SigDataOpts.PSEUDOSIG | Cms.SigDataOpts.ALT_ALGID | Cms.SigDataOpts.INCLUDE_ATTRS | Cms.SigDataOpts.ADD_SIGNTIME | Cms.SigDataOpts.ADD_SIGNINGCERT
    # NB privkey not required with PSEUDO option
    r = Cms.make_sigdata(pseudofile, "excontent.txt", "AliceRSASignByCarl.cer", "", Cms.SigAlg.RSA_SHA256, opts)
    print(f"Cms.make_sigdata(PSEUDOSIG) returns {r} (expected 0)")
    assert 0 == r
    print(f"Created file {pseudofile}")

    # Expecting bbbbbb... (this is *exactly* the correct length for the final signature)
    print("signatureValue: " + Cms.query_sigdata(pseudofile, "signatureValue"))
    # Check signing time (not required, but just to check, out of interest) NB UTC/GMT time
    print("signingTime: " + Cms.query_sigdata(pseudofile, "signingTime"))

    # Get digest value in hex - this is the digestValue over which the signature will be created.
    dighex = Cms.query_sigdata(pseudofile, "DigestOfSignedAttrs")
    print("DigestOfSignedAttrs: " + dighex)
    # Convert to base64
    digestvalue = Cnv.tobase64(Cnv.fromhex(dighex))
    print("digestValue: " + digestvalue)

    # Pass the digestValue in base64 encoding to the signing agency.
    # They will return the signatureValue (signInfo) in base64 created over the digestValue using "your" private key.
    # User: digestValue --> SigningAgency
    # SigningAgency: signatureValue --> User

    # OK, so we fiddle it here to compute the signatureValue ourselves using Alice's private key...
    signaturevalue = Sig.sign_digest(Cnv.frombase64(digestvalue), "AlicePrivRSASign.p8e", "password",
                                     Sig.Alg.RSA_SHA256)
    print("signatureValue: " + signaturevalue)

    # Now create a new signed-data file from the pseudo file and the received signature Value
    signedfile = "BasicSignByAlice_signed_from_pseudo.p7m"
    r = Cms.make_sigdata_from_pseudo(signedfile, pseudofile, Cnv.frombase64(signaturevalue))
    print(f"Cms.make_sigdata_from_pseudo returns {r} (expected 0)")
    assert 0 == r
    print(f"Created file {signedfile}")

    # Check the resulting file has a valid signature
    isok = Cms.verify_sigdata(signedfile)
    print(f"Cms.verify_sigdata returns {isok}")
    assert isok


def test_rsa_readjwk():
    print("\nREAD IN RSA KEY REPRESENTED AS JSON JWK...")
    # RSA public key as a JSON string
    # Ref: RFC 7517 JSON Web Key (JWK) Appendix A.1
    json = '''
    {"kty":"RSA",
    "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw",
    "e":"AQAB",
    "alg":"RS256",
    "kid":"2011-04-29"}
    '''
    print("JSON key=" + json)
    publickey = Rsa.read_public_key(json)
    assert len(publickey) > 0
    # Display some key properties
    print("RSA key size =", Rsa.key_bits(publickey))
    # Expecting 57F6BA24
    keyhashcode = Rsa.key_hashcode(publickey)
    print("KeyHashCode =", keyhashcode)
    assert keyhashcode == "57F6BA24"


def test_hash_length():
    print("\nTEST HASH LENGTH...")
    print("Hash.length(SHA-1) =", Hash.length(Hash.Alg.SHA1))
    print("Hash.length(SHA-256) =", Hash.length(Hash.Alg.SHA256))
    print("Hash.length(SHA-512) =", Hash.length(Hash.Alg.SHA512))
    print("Hash.length(RMD160) =", Hash.length(Hash.Alg.RMD160))


def test_kdf():
    print("\nTEST KEY DERIVATION FUNCTIONS...")
    # ansx963_2001.rsp CAVS 12.0 'ANS X9.63-2001' information for sample
    nbytes = 128 // 8
    zz = Cnv.fromhex("96c05619d56c328ab95fe84b18264b08725b85e33fd34f08")
    okhex = "443024c3dae66b95e6f5670601558f71"
    kek = Kdf.bytes(nbytes, zz, Kdf.KdfAlg.X963, Kdf.HashAlg.SHA256)
    print("KEK=", Cnv.tohex(kek))
    print("OK =", okhex)
    assert (Cnv.tohex(kek).lower() == okhex)

    # [RFC 5869] A.1.  Test Case 1 Basic test case with SHA-256
    nbytes = 42
    zz = Cnv.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")
    info = Cnv.fromhex("f0f1f2f3f4f5f6f7f8f9")
    okhex = "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865"
    kek = Kdf.bytes(nbytes, zz, Kdf.KdfAlg.HKDF, Kdf.HashAlg.SHA256, info, "salt=000102030405060708090a0b0c")
    print("KEK=", Cnv.tohex(kek))
    print("OK =", okhex)
    assert (Cnv.tohex(kek).lower() == okhex)

    # [RFC 5869] A.3.  Test with SHA-256 and zero-length salt/info
    nbytes = 42
    zz = Cnv.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")  # (22 octets)
    okhex = "8da4e775a563c18f715f802a063c5a31b8a11f5c5ee1879ec3454e5f3c738d2d9d201395faa4b61a96c8"
    kek = Kdf.bytes(nbytes, zz, Kdf.KdfAlg.HKDF, Kdf.HashAlg.SHA256)
    print("KEK=", Cnv.tohex(kek))
    print("OK =", okhex)
    assert (Cnv.tohex(kek).lower() == okhex)

    # Test Kdf.for_cms
    zz = Cnv.fromhex("160E3F5588C6FB4E9CEE8BC3C1C5000AB86396468C3D1CAEC0CB6E21536B5513")
    okhex = "04d616c654cdf62bb186a5a088b60fb5"
    kek = Kdf.for_cms(zz, Kdf.KeyWrapAlg.AES128_WRAP, Kdf.KdfAlg.X963, Kdf.HashAlg.SHA1)
    print("KEK=", Cnv.tohex(kek))
    print("OK =", okhex)
    assert (Cnv.tohex(kek).lower() == okhex)


def test_prf():
    print("\nTEST PRF FUNCTIONS...")
    # `KMAC_samples.pdf` "Secure Hashing - KMAC-Samples" 2017-02-27
    # Sample #1
    # "standard" KMAC output length KMAC128 => 256 bits, no custom string
    nbytes = 256 // 8
    msg = Cnv.fromhex("00010203")
    key = Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    okhex = "E5780B0D3EA6F7D3A429C5706AA43A00FADBD7D49628839E3187243F456EE14E"
    kmac = Prf.bytes(nbytes, msg, key, Prf.Alg.KMAC128)
    print("KMAC=", Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert Cnv.tohex(kmac).upper() == okhex, "KMAC failed"

    # "standard" KMAC output length KMAC256 => 512 bits, no custom string
    # Sample #6
    nbytes = 512 // 8
    # Length of data is 1600 bits
    msg = Cnv.fromhex("""000102030405060708090A0B0C0D0E0F
101112131415161718191A1B1C1D1E1F
202122232425262728292A2B2C2D2E2F
303132333435363738393A3B3C3D3E3F
404142434445464748494A4B4C4D4E4F
505152535455565758595A5B5C5D5E5F
606162636465666768696A6B6C6D6E6F
707172737475767778797A7B7C7D7E7F
808182838485868788898A8B8C8D8E8F
909192939495969798999A9B9C9D9E9F
A0A1A2A3A4A5A6A7A8A9AAABACADAEAF
B0B1B2B3B4B5B6B7B8B9BABBBCBDBEBF
C0C1C2C3C4C5C6C7""")
    key = Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    okhex = "75358CF39E41494E949707927CEE0AF20A3FF553904C86B08F21CC414BCFD691589D27CF5E15369CBBFF8B9A4C2EB17800855D0235FF635DA82533EC6B759B69"
    kmac = Prf.bytes(nbytes, msg, key, Prf.Alg.KMAC256)
    print("KMAC=", Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert Cnv.tohex(kmac).upper() == okhex, "KMAC failed"

    # Sample #2
    # Same as Sample #1 except with custom string
    nbytes = 256 // 8
    msg = Cnv.fromhex("00010203")
    key = Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    custom = "My Tagged Application"
    okhex = "3B1FBA963CD8B0B59E8C1A6D71888B7143651AF8BA0A7070C0979E2811324AA5"
    kmac = Prf.bytes(nbytes, msg, key, Prf.Alg.KMAC128, custom)
    print("KMAC=", Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert Cnv.tohex(kmac).upper() == okhex, "KMAC failed"

    # Request a lot of output (> single KECCAK block)
    nbytes = 1600 // 8
    msg = Cnv.fromhex("00010203")
    key = Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    okhex = """38158A1CAE4E1A25D85F2031246ADE69
7B3292FEF88B0923A59A02D1D53B7046
53EE7242662A10796BA20779D300D52D
7432018741233D587252D31DC48BDB82
33285D4A4ACD65848509B051A448D873
649228B6626E5EF817C7AF2DEDC91F12
0F8CA535A1EE301FAE8186FDEDE5A761
81A472A32CFAD1DDD1391E162F124D4A
7572AD8A20076601BCF81E4B0391F3E9
5AEFFA708C33C1217C96BE6A4F02FBBC
2D3B3B6FFAEB5BFD3BE4A2E02B75993F
CC04DA6FAC4BFCB2A9F05792A1A5CC80
CA34186243EFDB31"""
    okhex = okhex.replace("\n", "")
    kmac = Prf.bytes(nbytes, msg, key, Prf.Alg.KMAC128)
    print("KMAC=", Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert Cnv.tohex(kmac).upper() == okhex, "KMAC failed"


def test_xof():
    print("\nTEST XOF FUNCTIONS...")
    # Ref: "SHA-3 XOF Test Vectors for Byte-Oriented Output"
    # File `SHAKE256VariableOut.rsp` COUNT = 1244
    nbytes = 2000 // 8
    msg = Cnv.fromhex("6ae23f058f0f2264a18cd609acc26dd4dbc00f5c3ee9e13ecaea2bb5a2f0bb6b")
    okhex = """b9b92544fb25cfe4ec6fe437d8da2bbe
00f7bdaface3de97b8775a44d753c3ad
ca3f7c6f183cc8647e229070439aa953
9ae1f8f13470c9d3527fffdeef6c94f9
f0520ff0c1ba8b16e16014e1af43ac6d
94cb7929188cce9d7b02f81a2746f52b
a16988e5f6d93298d778dfe05ea0ef25
6ae3728643ce3e29c794a0370e9ca6a8
bf3e7a41e86770676ac106f7ae79e670
27ce7b7b38efe27d253a52b5cb54d6eb
4367a87736ed48cb45ef27f42683da14
0ed3295dfc575d3ea38cfc2a3697cc92
864305407369b4abac054e497378dd9f
d0c4b352ea3185ce1178b3dc1599df69
db29259d4735320c8e7d33e8226620c9
a1d22761f1d35bdff79a"""
    okhex = okhex.replace("\n", "")
    xof = Xof.bytes(nbytes, msg, Xof.Alg.SHAKE256)
    print("OUT=", Cnv.tohex(xof))
    print("OK =", okhex)
    assert (Cnv.tohex(xof).lower() == okhex)

    # Using MGF1-SHA-256
    # From SPHINCS+ test vectors r.3
    nbytes = 34
    msg = Cnv.fromhex("3b5c056af3ebba70d4c805380420585562b32410a778f558ff951252407647e3")
    okhex = "5b7eb772aecf04c74af07d9d9c1c1f8d3a90dcda00d5bab1dc28daecdc86eb87611e"
    xof = Xof.bytes(nbytes, msg, Xof.Alg.MGF1_SHA256)
    print("OUT=", Cnv.tohex(xof))
    print("OK =", okhex)
    assert Cnv.tohex(xof).lower() == okhex, "XOF failed"

    # Test other MGF1's
    nbytes = 24
    msg = Cnv.fromhex("012345ff")
    okhex = "242fb2e7a338ae07e580047f82b7acff83a41ec5d8ff9bab"
    xof = Xof.bytes(nbytes, msg, Xof.Alg.MGF1_SHA1)
    print("OUT=", Cnv.tohex(xof))
    print("OK =", okhex)
    assert Cnv.tohex(xof).lower() == okhex, "XOF failed"
    nbytes = 32
    msg = Cnv.fromhex("012345ff")
    okhex = "6855a6ab4f421ecb99857d31c4aa836bf3d4916ee8a71a168d3f4665f2d7b74c"
    xof = Xof.bytes(nbytes, msg, Xof.Alg.MGF1_SHA512)
    print("OUT=", Cnv.tohex(xof))
    print("OK =", okhex)
    assert Cnv.tohex(xof).lower() == okhex, "XOF failed"


def test_hkpe_labeled():
    print("\nTESTING HPKE LABELED{EXTRACT|EXPAND}...")
    print("RFC 9180 Appendix A.1 DHKEM(X25519, HKDF-SHA256), HKDF-SHA256, AES-128-GCM")
    print('prk = LabeledExtract("", "dkp_prk", ikm)')
    extracted = Hpke.labeled_extract(None, "dkp_prk",
                                     Cnv.fromhex("7268600d403fce431561aef583ee1613527cff655c1343f29812e66706df3234"),
                                     Hpke.CurveName.X25519)
    print("prk:", Cnv.tohex(extracted))
    assert Cnv.tohex(
        extracted).upper() == "7B8BFE1D6F3D0CB45C585E133299C64AC998BF46CAF2DC13BA874F23413EC23A", "labeled_extract failed"

    print("psk_id_hash = LabeledExtract('', 'psk_id_hash', '')")
    extracted = Hpke.labeled_extract(None, "psk_id_hash",
                                     None, Hpke.CurveName.X25519, Hpke.AeadAlg.AES_128_GCM)
    print("psk_id_hash:", Cnv.tohex(extracted))
    assert Cnv.tohex(
        extracted).lower() == "725611c9d98c07c03f60095cd32d400d8347d45ed67097bbad50fc56da742d07", "labeled_extract failed"

    print("key = LabeledExpand(secret, 'key', key_schedule_context, Nk)")
    nk = 16
    key = Hpke.labeled_expand(nk, Cnv.fromhex("12fff91991e93b48de37e7daddb52981084bd8aa64289c3788471d9a9712f397"),
                              "key",
                              Cnv.fromhex(
                                  "00725611c9d98c07c03f60095cd32d400d8347d45ed67097bbad50fc56da742d07cb6cffde367bb0565ba28bb02c90744a20f5ef37f30523526106f637abb05449"),
                              Hpke.CurveName.X25519, Hpke.AeadAlg.AES_128_GCM)
    print("key:", Cnv.tohex(key))
    assert Cnv.tohex(key).lower() == "4531685d41d65f03dc48f6b8302c05b0", "labeled_expand failed"


def test_hkpe_derive_private_key():
    print("\nTESTING HPKE DERIVEPRIVATEKEY...")
    print("RFC9180 A.1. DHKEM(X25519, HKDF-SHA256)")
    ikmhex = "7268600d403fce431561aef583ee1613527cff655c1343f29812e66706df3234"
    skokhex = "52c4a758a802cd8b936eceea314432798d5baf2d7e9235dc084ab1b9cfa2f736"
    pkokhex = "37fda3567bdbd628e88668c3c8d7e97d1d1253b6d4ea6d44c150f741f1bf4431"
    # A. Derive private key in hex format
    print("ikmE:", ikmhex)
    skhex = Hpke.derive_private_key(Cnv.fromhex(ikmhex), Hpke.CurveName.X25519, Hpke.OutputOpts.KEYASHEX)
    print("skEm:", skhex)
    assert skhex.lower() == skokhex, "HPKE derived key does not match test vector"
    # B. Derive key in ephemeral internal private key format (NB different each time)
    prikeystr = Hpke.derive_private_key(Cnv.fromhex(ikmhex), Hpke.CurveName.X25519)
    print("prikeystr:", prikeystr)
    print("curveName:", Ecc.query_key(prikeystr, "curveName"))
    # C. Get public key in hex format from internal key string
    pkhex = Ecc.query_key(prikeystr, "publicKey")
    print("pkEm:", pkhex)
    assert pkhex.lower() == pkokhex, "Public key does not match test vector"

    print("RFC9180 A.6. DHKEM(P-521, HKDF-SHA512)")
    ikmhex = "7f06ab8215105fc46aceeb2e3dc5028b44364f960426eb0d8e4026c2f8b5d7e7a986688f1591abf5ab753c357a5d6f0440414b4ed4ede71317772ac98d9239f70904"
    skokhex = "014784c692da35df6ecde98ee43ac425dbdd0969c0c72b42f2e708ab9d535415a8569bdacfcc0a114c85b8e3f26acf4d68115f8c91a66178cdbd03b7bcc5291e374b"
    pkokhex = "040138b385ca16bb0d5fa0c0665fbbd7e69e3ee29f63991d3e9b5fa740aab8900aaeed46ed73a49055758425a0ce36507c54b29cc5b85a5cee6bae0cf1c21f2731ece2013dc3fb7c8d21654bb161b463962ca19e8c654ff24c94dd2898de12051f1ed0692237fb02b2f8d1dc1c73e9b366b529eb436e98a996ee522aef863dd5739d2f29b0"
    # A. Derive private key in hex format
    print("ikmE:", ikmhex)
    skhex = Hpke.derive_private_key(Cnv.fromhex(ikmhex), Hpke.CurveName.P_521, Hpke.OutputOpts.KEYASHEX)
    print("skEm:", skhex)
    assert skhex.lower() == skokhex, "HPKE derived key does not match test vector"
    # B. Derive key in ephemeral internal private key format (NB different each time)
    prikeystr = Hpke.derive_private_key(Cnv.fromhex(ikmhex), Hpke.CurveName.P_521)
    print("prikeystr:", prikeystr)
    print("curveName:", Ecc.query_key(prikeystr, "curveName"))
    # C. Get public key in hex format from internal key string
    pkhex = Ecc.query_key(prikeystr, "publicKey")
    print("pkEm:", pkhex)
    assert pkhex.lower() == pkokhex, "Public key does not match test vector"


def test_cms_makeenvdata_ecdh():
    print("\nMAKE ENVELOPED-DATA OBJECTS USING ECDH KARI...")
    # Create an enveloped CMS object to Dana (using ecdh) and Alice (using RSA)
    fname = "dana_alice_all_defaults.p7m"
    certlist = "lamps-dana.encrypt.crt;lamps-alice.encrypt.crt"
    msg = "This is some sample content."
    n = Cms.make_envdata_from_string(fname, msg, certlist, Cipher.Alg.AES128)
    print("Cms.make_envdata_from_string returns", n, " (expecting 2)")
    assert n > 0
    print("FILE:", fname)

    # Query the enveloped-data file
    query = "contentEncryptionAlgorithm"
    s = Cms.query_envdata(fname, query)
    print(f"{query}='{s}'")
    query = "recipientInfoType"
    s = Cms.query_envdata(fname, query)
    print(f"{query}='{s}'")
    query = "recipientInfoType/2"
    s = Cms.query_envdata(fname, query)
    print(f"{query}='{s}'")
    query = "keyEncryptionAlgorithm"
    s = Cms.query_envdata(fname, query)
    print(f"{query}='{s}'")
    query = "keyEncryptionAlgorithm/2"
    s = Cms.query_envdata(fname, query)
    print(f"{query}='{s}'")

    # Read back from CMS enveloped-data object using private keys
    print("Read CMS using Alice's RSA private key:")
    prikeyalice = Rsa.read_private_key("lamps-alice.decrypt.p8.pem", "")
    s = Cms.read_envdata_to_string(fname, prikeyalice, "lamps-alice.encrypt.crt")
    print("MSG =", s)
    assert (len(s) > 0)
    print("Read CMS using Dana's ECC X25519 private key:")
    prikeydana = Ecc.read_private_key("lamps-dana.decrypt.p8.pem", "")
    s = Cms.read_envdata_to_string(fname, prikeydana, "lamps-dana.encrypt.crt")
    print("MSG =", s)
    assert (len(s) > 0)


def test_x509_makecert_internal_x25519():
    print("\nCREATE A NEW CERTIFICATE USING INTERNAL KEY STRINGS WITH X25519...")
    certname = "new-lamps-dana.encrypt.cer"
    issuercert = "lamps-ca.ed25519.crt"
    prikeyfile = "lamps-ca.ed25519.p8"
    pubkeyfile = "lamps-dana.encrypt.crt"
    dn = "O=IETF;OU=LAMPS WG;CN=Dana Hopper"
    # sMIMECapabilities = ECDH with HKDF using SHA-256; uses AES-128 key wrap
    extns = "serialNumber=#x0E4B0A36A9EFBA9C9A3B68248E521DC0DEF3A7;notBefore=2020-12-15T21:35:44;notAfter=2052-12-15T21:35:44;extKeyUsage=emailProtection;" \
            + "keyUsage=keyAgreement;sMIMECapabilities=301A060B2A864886F70D0109100313300B0609608648016503040105;" \
            + "certificatePolicies=2.16.840.1.101.3.2.1.48.1;rfc822Name=dana@smime.example;subjectKeyIdentifier=9ddf4dd405ef9aec6086bc276d04e9ce5adc8fa4;"
    # Read in private and public keys to internal key strings
    prikeystr = Ecc.read_private_key(prikeyfile, "")
    print("prikeystr=", prikeystr)
    print("PRI: keyBits=", Ecc.query_key(prikeystr, "keyBits"), ", curveName =", Ecc.query_key(prikeystr, "curveName"),
          ", keyHashCode=", Ecc.key_hashcode(prikeystr))
    assert (len(prikeystr) > 0)
    pubkeystr = Ecc.read_public_key(pubkeyfile)
    print("PUB: keyBits=", Ecc.query_key(pubkeystr, "keyBits"), ", curveName =", Ecc.query_key(pubkeystr, "curveName"),
          ", keyHashCode=", Ecc.key_hashcode(pubkeystr))
    assert (len(pubkeystr) > 0)
    print("dn='" + dn + "'")
    print("extns='" + extns + "'")
    # Create the new certificate
    try:
        r = X509.make_cert(certname, issuercert, pubkeystr, prikeystr, "", distname=dn, extns=extns,
                           sigalg=X509.SigAlg.ED25519, opts=X509.Opts.AUTHKEYID)
        print("X509.make_cert returns", r)
    except PKIError as e:
        print("Woops! PKIError:", e)
    # print(Asn1.text_dump_tostring(certname))
    print("FILE:", certname)
    query = "subjectPublicKeyAlgorithm"
    print(query + "='" + X509.query_cert(certname, query) + "'")
    query = "signatureAlgorithm"
    print(query + "='" + X509.query_cert(certname, query) + "'")
    print(X509.text_dump_tostring(certname))


def test_cms_envdata_auth():
    print("\nAUTHENTICATED-ENVELOPED-DATA OBJECTS...")
    # Create an authenticated-enveloped CMS object to Bob using Bob's X.509 certificate
    fname = "cms2bob_auth.p7m"
    fnamecert = "BobRSASignByCarl.cer"
    s = "This is some sample content."

    n = Cms.make_envdata_from_string(fname, s, fnamecert, Cipher.Alg.AES128, Cms.KeyEncrAlg.RSA_PKCS1V1_5,
                                     0, Cms.EnvDataOpts.AUTHENTICATED, count=13)
    print("Cms.make_envdata_from_string returns", n)
    assert (n == 1)
    print(Asn1.text_dump_tostring(fname))


def test_cms_make_envdata_auth_chapoly():
    print("\nAUTHENTICATED-ENVELOPED-DATA USING CHACHA20POLY1305...")
    filein = "excontent.txt"
    cmsfile = "cms2bob_auth_chapoly.p7m"
    certfile = "lamps-bob.crt"
    keyfile = "lamps-bob.p8"  # Unencrypted
    n = Cms.make_envdata(cmsfile, filein, certfile, Cms.ContentEncrAlg.CHACHA20_POLY1305)
    assert n == 1  # Expecting one recipient
    print("Created file:", cmsfile)
    print(Asn1.type(cmsfile))
    print("contentEncryptionAlgorithm:", Cms.query_envdata(cmsfile, "contentEncryptionAlgorithm"))
    print("keyEncryptionAlgorithm:", Cms.query_envdata(cmsfile, "keyEncryptionAlgorithm"))
    # print(Asn1.text_dump_tostring(cmsfile))
    # Now try and read it
    prikeystr = Rsa.read_private_key(keyfile)
    decstr = Cms.read_envdata_to_string(cmsfile, prikeystr)
    assert len(decstr) > 0
    print(f"DEC: '{decstr}'")

    # Now use X25519
    print("\nUsing X25519...")
    cmsfile = "cms2carlos_auth_chapoly_X25519.p7m"
    certfile = "lamps-carlos.encrypt.cer"
    keyfile = "lamps-carlos.decrypt.p8"  # Unencrypted
    n = Cms.make_envdata(cmsfile, filein, certfile, Cms.ContentEncrAlg.CHACHA20_POLY1305, kdfalg=Kdf.KdfAlg.HKDF)
    assert n == 1  # Expecting one recipient
    print("Created file:", cmsfile)
    print(Asn1.type(cmsfile))
    print("contentEncryptionAlgorithm:", Cms.query_envdata(cmsfile, "contentEncryptionAlgorithm"))
    print("keyEncryptionAlgorithm:", Cms.query_envdata(cmsfile, "keyEncryptionAlgorithm"))
    print("originatorKeyAlgorithm:", Cms.query_envdata(cmsfile, "originatorKeyAlgorithm"))
    # print(Asn1.text_dump_tostring(cmsfile))
    # Now try and read it
    prikeystr = Ecc.read_private_key(keyfile)
    decstr = Cms.read_envdata_to_string(cmsfile, prikeystr)
    assert len(decstr) > 0
    print(f"DEC: '{decstr}'")

    print("\nUsing X448...")
    cmsfile = "cms2alice_auth_chapoly_X448.p7m"
    certfile = "X448-alice-self-issued.cer"
    keyfile = "X448-alice-self.p8"  # Unencrypted
    n = Cms.make_envdata(cmsfile, filein, certfile, Cms.ContentEncrAlg.CHACHA20_POLY1305, hashalg=Hash.Alg.SHA512,
                         kdfalg=Kdf.KdfAlg.HKDF)
    assert n == 1  # Expecting one recipient
    print("Created file:", cmsfile)
    print(Asn1.type(cmsfile))
    print("keyEncryptionAlgorithm:", Cms.query_envdata(cmsfile, "keyEncryptionAlgorithm"))
    print("originatorKeyAlgorithm:", Cms.query_envdata(cmsfile, "originatorKeyAlgorithm"))
    # print(Asn1.text_dump_tostring(cmsfile))
    # Now try and read it
    prikeystr = Ecc.read_private_key(keyfile)
    decstr = Cms.read_envdata_to_string(cmsfile, prikeystr)
    assert len(decstr) > 0
    print(f"DEC: '{decstr}'")


def test_cms_envdata_examples():
    print("\nENVELOPED-DATA EXAMPLES USED IN DOCS...")
    print("Create an enveloped CMS object (ktri type) to Bob using Bob's RSA key..")
    n = Cms.make_envdata("cms2bob_aes128.p7m", "excontent.txt", "BobRSASignByCarl.cer", Cipher.Alg.AES128,
                         Cms.KeyEncrAlg.RSA_OAEP)
    print("Cms.make_envdata returns", n)
    assert (n == 1)
    fname = "cms2bob_aes128.p7m"
    print("FILE:", fname)
    query = "recipientInfoType"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))
    query = "contentEncryptionAlgorithm"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))

    print("Same but using authenticated encryption and creating an authEnvelopedData object..")
    n = Cms.make_envdata("cms2bob_aes128auth.p7m", "excontent.txt", "BobRSASignByCarl.cer", Cms.ContentEncrAlg.AES_128_GCM,
                         Cms.KeyEncrAlg.RSA_OAEP)
    assert (n == 1)
    fname = "cms2bob_aes128auth.p7m"
    print("FILE:", fname)
    query = "recipientInfoType"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))
    query = "contentEncryptionAlgorithm"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))

    print("Create an enveloped CMS object (kari type) to Dana using Dana's ECC key..")
    n = Cms.make_envdata("cms2dana_hkdf.p7m", "excontent.txt", "lamps-dana.encrypt.crt", Cipher.Alg.AES256,
                         hashalg=Hash.Alg.SHA256, kdfalg=Kdf.KdfAlg.HKDF,
                         keywrapalg=Kdf.KeyWrapAlg.AES256_WRAP)
    print("Cms.make_envdata returns", n)
    assert (n == 1)
    fname = "cms2dana_hkdf.p7m"
    print("FILE:", fname)
    query = "recipientInfoType"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))
    query = "contentEncryptionAlgorithm"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))

    print(
        "Create an enveloped CMS object (kekri type) using a previously distributed symmetric key-encryption key (KEK)..")
    n = Cms.make_envdata("cms_envdata_kekri.p7m", "excontent.txt", "type=@kekri,keyid=ourcommonkey",
                         Cipher.Alg.AES256, hashalg=Hash.Alg.SHA256,
                         keywrapalg=Kdf.KeyWrapAlg.AES128_WRAP, keyString="#x0123456789ABCDEFF0E1D2C3B4A59687")
    print("Cms.make_envdata returns", n)
    assert (n == 1)
    fname = "cms_envdata_kekri.p7m"
    print("FILE:", fname)
    query = "recipientInfoType"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))
    query = "contentEncryptionAlgorithm"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))
    query = "keyid"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))

    print("Create an enveloped CMS object (pwri type) using password-based key management..")
    n = Cms.make_envdata("cms_envdata_pwri.p7m", "excontent.txt", "type=@pwri", Cipher.Alg.AES192,
                         keyString="password12345")
    print("Cms.make_envdata returns", n)
    assert (n == 1)
    fname = "cms_envdata_pwri.p7m"
    print("FILE:", fname)
    query = "recipientInfoType"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))
    query = "contentEncryptionAlgorithm"
    print("%s=%s" % (query, Cms.query_envdata(fname, query)))

    print("\nNow read in the enveloped-data objects we made above...")
    prikeystr = Rsa.read_private_key("BobPrivRSAEncrypt.p8e", "password")
    assert (len(prikeystr) > 0)
    fname = "cms2bob_aes128.p7m"
    print("FILE:", fname)
    s = Cms.read_envdata_to_string(fname, prikeystr)
    print("MSG='%s'" % s)
    assert (len(s) > 0)
    fname = "cms2bob_aes128auth.p7m"
    print("FILE:", fname)
    s = Cms.read_envdata_to_string(fname, prikeystr)
    print("MSG='%s'" % s)
    assert (len(s) > 0)
    prikeystr = Ecc.read_private_key("lamps-dana.decrypt.p8.pem", "")
    assert (len(prikeystr) > 0)
    fname = "cms2dana_hkdf.p7m"
    print("FILE:", fname)
    s = Cms.read_envdata_to_string(fname, prikeystr)
    print("MSG='%s'" % s)
    assert (len(s) > 0)
    fname = "cms_envdata_kekri.p7m"
    print("FILE:", fname)
    s = Cms.read_envdata_to_string(fname, "#x0123456789ABCDEFF0E1D2C3B4A59687")
    print("MSG='%s'" % s)
    assert (len(s) > 0)
    fname = "cms_envdata_pwri.p7m"
    print("FILE:", fname)
    s = Cms.read_envdata_to_string(fname, "password12345")
    print("MSG='%s'" % s)
    assert (len(s) > 0)


def test_cnv_shortpathname():
    print("\nGET SHORT NAME PATH...")

    shortname = Cnv.shortpathname("你好.txt")
    print("shortname='%s'" % shortname)
    exists = os.path.exists(shortname)  # Fixed [2023-04-19]
    print("File '" + shortname + "' " + "EXISTS" if exists else "does not exists")
    assert (exists)

    shortname = Cnv.shortpathname("File with a long name and spaces hello there all good yes thanks.txt")
    print("shortname='%s'" % shortname)
    exists = os.path.exists(shortname)  # Fixed [2023-04-19]
    print("File '" + shortname + "' " + "EXISTS" if exists else "does not exists")
    assert (exists)


def test_gen_format_error_message():
    print("\nTEST FORMAT ERROR MESSAGE...")
    # Try and read missing file
    try:
        s = Asn1.type("missing.file")
    except PKIError as e:
        print(e)
    # ERROR CODE 1: Cannot open input file (OPEN_ERROR): Unable to open file 'missing.file'

    # Attempt to create signed data but pass name of missing certificate file
    privkey = Rsa.read_private_key('AlicePrivRSASign.p8e', 'password')
    try:
        r = Cms.make_sigdata('sigdata.p7m', 'excontent.txt', 'missing.file', privkey)
        print("Cms.make_sigdata succeeded returning ", r)  # Shouldn't happen
    except PKIError as e:
        print(e)
    # ERROR CODE 21: No match found (NO_MATCH_ERROR): (1) Cannot open input file (OPEN_ERROR):
    # Private key does not match any certificate in list


def test_rsa_read_public_key_csr():
    print("\nREAD PUBLIC KEY FROM CSR...")
    # Create a new CSR for LAMPS WG alice
    csrfile = "lamps-alice-csr.pem"
    keyfile = "lamps-alice.p8"  # No password
    dn = "O=IETF;OU=LAMPS WG;CN=Alice Lovelace;"
    extns = "keyUsage=digitalSignature,nonRepudiation;extKeyUsage=emailProtection"

    r = X509.cert_request(csrfile, keyfile, "", dn, extns, X509.SigAlg.RSA_SHA256)
    print(f"X509.cert_request created file '{csrfile}'")
    # Dump details of CSR we just made...
    print(X509.text_dump_tostring(csrfile, X509.Opts.LDAP))

    # New in [v20.7]: Read in public key from this CSR file to an internal key string
    keystr = Rsa.read_public_key(csrfile)
    print("Keysize=" + str(Rsa.key_bits(keystr)) + " bits, HashCode=0x" + Rsa.key_hashcode(keystr))
    # Keysize=2048 bits, HashCode=0xCA0B84DA


def test_x509_make_cert_448():
    print("\nMAKE X.509 CERT USING CURVE448:")
    # 1. Create a self-signed certificate using the Ed448 key
    prikeyfile = "edkey448.p8"
    certfile = "Ed448-self.cer"
    dn = "CN=example.com"
    extns = "notBefore=2023-01-01;notAfter=2040-12-31;"
    # Digital Signature, Certificate Signing, [Off-line CRL Signing], CRL Signing
    # keyusage = X509.KeyUsageFlags.DIGITALSIGNATURE | X509.KeyUsageFlags.KEYCERTSIGN | X509.KeyUsageFlags.CRLSIGN
    extns += "keyUsage=digitalSignature,keyCertSign,cRLSign;"
    r = X509.make_cert_self(certfile, prikeyfile, "", 0x0ED448, 0, dn, extns, sigalg=X509.SigAlg.ED448,
                            opts=X509.Opts.UTF8)
    print("Created self-signed X.509 certificate:", certfile)
    print(X509.text_dump_tostring(certfile, X509.Opts.LDAP))
    print("issuerName:", X509.query_cert(certfile, "issuerName"))
    print("subjectName:", X509.query_cert(certfile, "subjectName"))
    print("subjectPublicKeyAlgorithm:", X509.query_cert(certfile, "subjectPublicKeyAlgorithm"))
    print("signatureAlgorithm:", X509.query_cert(certfile, "signatureAlgorithm"))

    # 2. Now create a self-*issued* cert using Ed448 to sign an X448 public key
    print("\nAbout to create a *self-issued* cert using Ed448 to sign an X448 public key...")
    # Read in the public key from its hex value
    pubkeystr = Ecc.read_key_by_curve(
        "9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0",
        Ecc.CurveName.X448, ispublic=True)
    assert len(pubkeystr) > 0
    dn = "CN=Alice X448;O=example.com"
    extns = "notBefore=2023-07-01T12:19:24;notAfter=2040-12-31T23:59:58;keyUsage=noncritical;serialNumber=#x5601474A2A8DC330;" \
            + "subjectKeyIdentifier=DEADBEEFCAFEBABE"
    keyusage = X509.KeyUsageFlags.KEYAGREEMENT
    issuercert = certfile  # Created above
    certfile = "X448-self-issued.cer"
    # Create self-issued cert containing Alice's X448 public key but signed by Ed448 cert
    r = X509.make_cert(certfile, issuercert, pubkeystr, prikeyfile, "", 0, 0, dn, extns, keyusage,
                       X509.SigAlg.ED448, opts=X509.Opts.UTF8)
    print("Created self-issued X.509 certificate:", certfile)
    # print(X509.text_dump_tostring(certfile, X509.Opts.LDAP))
    print("issuerName:", X509.query_cert(certfile, "issuerName"))
    print("subjectName:", X509.query_cert(certfile, "subjectName"))
    print("subjectPublicKeyAlgorithm:", X509.query_cert(certfile, "subjectPublicKeyAlgorithm"))
    print("signatureAlgorithm:", X509.query_cert(certfile, "signatureAlgorithm"))

    # Verify that self-issued cert was signed by issuer
    print("Verify the certificate against its issuer...")
    isok = X509.cert_is_verified(certfile, issuercert)
    print("X509.cert_is_verified returns", isok)
    assert isok


def test_scrypt():
    print("\nTESTING SCRYPT PASSWORD-BASED KEY DERIVATION FUNCTION...")
    # Use SCRYPT examples from RFC7914
    dk = Pbe.scrypt(64, b'password', b'NaCl', 1024, 8, 16)
    print("dk(SCRYPT)=", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == 'FDBABE1C9D3472007856E7190D01E9FE7C6AD7CBC8237830E77376634B373162' \
           + '2EAF30D92E22A3886FF109279D9830DAC727AFB94A83EE6D8360CBDFA2CC0640'
    # Pass empty string for both password and salt with (N=16, r=1, p=1)
    dk = Pbe.scrypt(64, b'', b'', 16, 1, 1)
    print("dk(SCRYPT)=", Cnv.tohex(dk))
    assert Cnv.tohex(dk) == '77D6576238657B203B19CA42C18A0497F16B4844E3074AE8DFDFFA3FEDE21442' \
           + 'FCD0069DED0948F8326A753A0FC81F17E8D3E0FB2E0D3628CF35E20C38D18906'


def test_ecc_make_keys_448():
    print("\nTESTING MAKE KEYS FOR ED448 and X448...")
    pubkeyfile = "myed448.pub"
    prikeyfile = "myed448.p8e"
    pwd = "password"
    n = Ecc.make_keys(pubkeyfile, prikeyfile, Ecc.CurveName.ED448, pwd, pbescheme=Ecc.PbeScheme.PBKDF2_AES256)
    assert (0 == n)
    _dump_and_print_asn1(pubkeyfile)
    print(pubkeyfile + ": " + Asn1.type(pubkeyfile))
    print(prikeyfile + ": " + Asn1.type(prikeyfile))
    # Read in private key as internal key string
    skstr = Ecc.read_private_key(prikeyfile, pwd)
    print("sk curve =", Ecc.query_key(skstr, "curveName"), "keyhashcode =", Ecc.key_hashcode(skstr))
    pkstr = Ecc.read_public_key(pubkeyfile)
    print("pk curve =", Ecc.query_key(pkstr, "curveName"), "keyhashcode =", Ecc.key_hashcode(pkstr))

    pubkeyfile = "myX448.pub"
    prikeyfile = "myX448.p8e"
    pwd = "password"
    n = Ecc.make_keys(pubkeyfile, prikeyfile, Ecc.CurveName.X448, pwd, pbescheme=Ecc.PbeScheme.PBKDF2_AES256)
    assert (0 == n)
    _dump_and_print_asn1(pubkeyfile)
    print(pubkeyfile + ": " + Asn1.type(pubkeyfile))
    print(prikeyfile + ": " + Asn1.type(prikeyfile))
    # Read in private key as internal key string
    skstr = Ecc.read_private_key(prikeyfile, pwd)
    print("sk curve =", Ecc.query_key(skstr, "curveName"), "keyhashcode =", Ecc.key_hashcode(skstr))
    pkstr = Ecc.read_public_key(pubkeyfile)
    print("pk curve =", Ecc.query_key(pkstr, "curveName"), "keyhashcode =", Ecc.key_hashcode(pkstr))


def test_ecc_readbycurve_448():
    print("\nTESTING READBYCURVE FOR ED448 and X448...")
    prikeystr = Ecc.read_key_by_curve(
        "c4eab05d357007c632f3dbb48489924d 552b08fe0c353a0d4a1f00acda2c463a fbea67c5e8d2877c5e3bc397a659949e f8021e954e0a12274e",
        Ecc.CurveName.ED448, ispublic=False)
    assert len(prikeystr) > 0
    print("CURVE: ", Ecc.query_key(prikeystr, "curveName"))
    print("KeyHashCode:", Ecc.key_hashcode(prikeystr))
    print("SK: ", Ecc.query_key(prikeystr, "privateKey"))
    print("PK: ", Ecc.query_key(prikeystr, "publicKey"))
    # Read in corresponding public key
    pubkeystr = Ecc.read_key_by_curve(
        "43ba28f430cdff456ae531545f7ecd0ac834a55d9358c0372bfa0c6c6798c0866aea01eb00742802b8438ea4cb82169c235160627b4c3a9480",
        Ecc.CurveName.ED448, ispublic=True)
    assert len(pubkeystr) > 0
    print("CURVE: ", Ecc.query_key(pubkeystr, "curveName"))
    print("KeyHashCode:", Ecc.key_hashcode(pubkeystr))

    # Again for ECDH X448 key
    prikeystr = Ecc.read_key_by_curve(
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        Ecc.CurveName.X448, ispublic=False)
    assert len(prikeystr) > 0
    print("CURVE: ", Ecc.query_key(prikeystr, "curveName"))
    print("KeyHashCode:", Ecc.key_hashcode(prikeystr))
    print("SK: ", Ecc.query_key(prikeystr, "privateKey"))
    print("PK: ", Ecc.query_key(prikeystr, "publicKey"))
    # Read in corresponding public key
    pubkeystr = Ecc.read_key_by_curve(
        "172837c1ef0bf5d890af8dcee6bda1ad1970c167e893dd46054795693a11397580fe732f2b50bd9fc1d7596c62fd5c4d5df403e94ad8c507",
        Ecc.CurveName.X448, ispublic=True)
    assert len(pubkeystr) > 0
    print("CURVE: ", Ecc.query_key(pubkeystr, "curveName"))
    print("KeyHashCode:", Ecc.key_hashcode(pubkeystr))


def test_ecc_savekeys_448():
    print("\nTESTING SAVEKEYS FOR CURVE448...")
    # Read in private key from hex representation
    prikeystr = Ecc.read_key_by_curve(
        "9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28dd9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b",
        Ecc.CurveName.X448, ispublic=False)
    assert len(prikeystr) > 0
    print("CURVE: ", Ecc.query_key(prikeystr, "curveName"))
    print("KeyHashCode:", Ecc.key_hashcode(prikeystr))
    print("SK: ", Ecc.query_key(prikeystr, "privateKey"))
    print("PK: ", Ecc.query_key(prikeystr, "publicKey"))
    # Save to unencrypted PKCS8 v2 file (OneAsymmetricKey)
    # [v22.0] by default now includes the public key as well
    fname = "keypri_X448.p8"
    r = Ecc.save_key(fname, prikeystr)
    print(f"Created key file '{fname}'")
    print(Asn1.type(fname))
    print(Asn1.text_dump_tostring(fname))
    # Check we can read the private key
    prikeystr = Ecc.read_private_key(fname)
    assert len(prikeystr) > 0
    print("KeyHashCode:", Ecc.key_hashcode(prikeystr))
    print("Is a Private Key" if Ecc.query_key(prikeystr, "isPrivate") else "Is a Public Key")
    # Check we can read the public key
    pubkeystr = Ecc.read_public_key(fname)
    assert len(pubkeystr) > 0
    print("KeyHashCode:", Ecc.key_hashcode(pubkeystr))
    print("Is a Private Key" if Ecc.query_key(pubkeystr, "isPrivate") else "Is a Public Key")

    # Now save in legacy v1 PKCS8 without public key
    fname = "keypri_X448_legacy.p8"
    r = Ecc.save_key(fname, prikeystr, keytype=Ecc.KeyType.LEGACY)
    print(f"Created key file '{fname}'")
    print(Asn1.type(fname))
    print(Asn1.text_dump_tostring(fname))


def test_pfx_makefile_double():
    print("\nTESTING MAKE PFX LIKE PARAGUAY CA'S DO...")
    epkfile = "sifen-emisor.p8e"
    certfile = "sifen-emisor.cer"
    pwd = "12345678a"
    pfxfile = "sifen-emisor.p12"
    # Make a PFX like Paraguay SET CA's (unencrypted cert + double-encrypted key)
    n = Pfx.make_file(pfxfile, certfile, epkfile, pwd, "EMPRESA DE AUTOBUSES",
                      Pfx.Opts.DOUBLE_ENCRYPT | Pfx.Opts.PLAIN_CERT)
    assert (0 == n)
    print("Created new PKCS#12 file:", pfxfile)
    print("Asn1.Type(" + pfxfile + ") -->", Asn1.type(pfxfile))
    # print(Asn1.text_dump_tostring(pfxfile))
    # Make sure we can read both the private key and certificate
    prikeystr = Rsa.read_private_key(pfxfile, pwd)
    assert len(prikeystr) > 0
    print("Key size =", Rsa.key_bits(prikeystr))
    certstr = X509.read_cert_string_from_pfx(pfxfile, pwd)
    assert len(certstr) > 0
    print("Cert subject =", X509.query_cert(certstr, "subjectName", opts=X509.Opts.LDAP))


# Explicity call this function to test the Pwd dialog class
# Note this does not begin with `test_` because we don't want it firing in py.test
def do_pwd():
    print("\nTESTING PWD DIALOG...")
    pwd = Pwd.prompt()
    print("[" + pwd + "]")
    pwd = Pwd.prompt("Demo of Pwd.prompt()", "Type secret phrase:")
    print("[" + pwd + "]")


def quick_version():
    print("\nDETAILS OF CORE DLL...")
    print("DLL Version=" + str(Gen.version())
          + " [" + Gen.core_platform() + "] Lic="
          + Gen.licence_type()
          + " Compiled=["
          + Gen.compile_time() + "]")
    print("[" + Gen.module_name() + "]" + " (" + Gen.module_info() + ")")


def main():
    do_all = True
    for arg in sys.argv:
        global delete_tmp_dir
        if (arg == 'nodelete'):
            delete_tmp_dir = False
        elif (arg == 'some'):
            do_all = False
    setup_temp_dir()

    # DO THE TESTS - EITHER SOME OR ALL
    if (do_all):
        test_version()
        test_error_lookup()
        test_cnv()
        test_cnv_utf8()
        test_cipher()
        test_cipher_block()
        test_cipher_file()
        test_cipher_keywrap()
        test_cipher_pad()
        test_rsa_makekeys()
        test_rsa_errors()
        test_rsa_savekeys()
        test_rsa_sign()
        test_rsa_encrypt()
        test_rng()
        test_hash()
        test_hmac()
        test_x509_generate()
        test_x509_analyze()
        test_x509_validate()
        test_x509_extract()
        test_wipe()
        test_asn1()
        test_ocsp()
        test_ecc()
        test_pbe()
        test_pfx()
        test_pem()
        test_cms_envdata()
        test_cms_sigdata()
        test_cms_comprdata()
        test_smime()
        test_sig_rsa()
        test_sig_ecc()
        test_x509_ecc()
        test_asn1_dumptostring()
        test_compress()
        test_aead()
        test_readcertstring()
        test_cipher_prefix()
        test_x509_makecert_emptydn()
        test_x509_certrequest_emptydn_extkeyusage()
        test_read_x509_from_pfx_3des()
        test_pfx_makefile_3des()
        test_rng_guid()
        test_ecc_dh_shared_secret()
        test_ecc_dh_shared_secret_x25519()
        test_cipher_hex()
        test_sig_signdata_ed25519()
        test_cms_makesigdata_ed25519()
        test_x509_makecertself_25519()
        test_cms_pseudo()
        test_rsa_readjwk()
        test_ecc_brainpool()
        test_hash_length()
        test_kdf()
        test_cms_makeenvdata_ecdh()
        test_x509_makecert_internal_x25519()
        test_cms_envdata_auth()
        test_cms_envdata_examples()
        test_cnv_shortpathname()
        test_gen_format_error_message()
        test_cipher_gcm()
        test_rsa_read_public_key_csr()
        test_hash_sha3()
        test_hmac_sha3()
        test_prf()
        test_xof()
        test_scrypt()
        test_pfx_makefile_double()
        test_ecc_make_keys_448()
        test_ecc_readbycurve_448()
        test_ecc_savekeys_448()
        test_ecc_dh_shared_secret_x448()
        test_x509_make_cert_448()
        test_sig_signdata_ed448()
        test_cms_makesigdata_ed448()
        test_hkpe_labeled()
        test_hkpe_derive_private_key()
        test_aead_chapoly()
        test_cms_make_envdata_auth_chapoly()

    else:  # just do some tests: comment out as necessary
        test_version()
        # test_error_lookup()
        # test_cnv()
        # test_cnv_utf8()
        # test_cipher()
        # test_cipher_block()
        # test_cipher_file()
        # test_cipher_keywrap()
        # test_cipher_pad()
        # test_rsa_makekeys()
        # test_rsa_errors()
        # test_rsa_savekeys()
        # test_rsa_sign()
        # test_rsa_encrypt()
        # test_rng()
        # test_hash()
        # test_hmac()
        # test_x509_generate()
        # test_x509_analyze()
        # test_x509_validate()
        # test_x509_extract()
        # test_wipe()
        # test_asn1()
        # test_ocsp()
        # test_ecc()
        # test_pbe()
        # test_pfx()
        # test_pem()
        # test_cms_envdata()
        # test_cms_sigdata()
        # test_cms_comprdata()
        # test_smime()
        # test_sig_rsa()
        # test_sig_ecc()
        # test_x509_ecc()
        # test_asn1_dumptostring()
        # test_compress()
        # test_aead()
        # test_readcertstring()
        # test_cipher_prefix()
        # test_x509_makecert_emptydn()
        # test_x509_certrequest_emptydn_extkeyusage()
        # test_read_x509_from_pfx_3des()
        # test_pfx_makefile_3des()
        # test_rng_guid()
        # test_ecc_dh_shared_secret()
        # test_ecc_dh_shared_secret_x25519()
        # test_cipher_hex()
        # test_sig_signdata_ed25519()
        # test_cms_makesigdata_ed25519()
        # test_x509_makecertself_25519()
        # test_cms_pseudo()
        # test_rsa_readjwk()
        # test_ecc_brainpool()
        # New in [v20.5]
        # test_hash_length()
        # test_kdf()
        # test_cms_makeenvdata_ecdh()
        # test_x509_makecert_internal_x25519()
        # # New in [v20.6]
        # test_cms_envdata_auth()
        # test_cms_envdata_examples()
        # # New in [v21.0]
        # test_cnv_shortpathname()
        # test_gen_format_error_message()
        # test_cipher_gcm()
        # test_rsa_read_public_key_csr()
        # test_x509_make_cert_ex()
        # test_hash_sha3()
        # test_hmac_sha3()
        # test_prf()
        # test_xof()
        # # New in [v22.0]
        # test_scrypt()
        # test_pfx_makefile_double()
        # test_ecc_make_keys_448()
        # test_ecc_readbycurve_448()
        # test_ecc_savekeys_448()
        # test_ecc_dh_shared_secret_x448()
        # test_x509_make_cert_448()
        # test_sig_signdata_ed448()
        # test_cms_makesigdata_ed448()
        # test_hkpe_labeled()
        # test_hkpe_derive_private_key()
        # test_aead_chapoly()
        test_cms_make_envdata_auth_chapoly()

        # Uncomment the next line to test the Pwd dialog procedure
        # Do not do in py.test (unless you want to interact!)
        # ## do_pwd()
    reset_start_dir()
    quick_version()
    print("__version__=", pki.__version__)
    print("ALL DONE.")


if __name__ == "__main__":
    main()
