import port_scanner
import os
import sys
import pytest
# Tests require active internet connection. Uses online resources like en.wikipedia.org or the localhost
def test_localhost():
    #setup
    sys.stdout = open('temp.txt', 'w')
    port_scanner.main(["", "localhost", "0", "1000"])    
    sys.stdout = sys.__stdout__
    output = open("temp.txt", 'r').read()
    #assertions for tests
    assert "localhost is online" in output
    #teardown
    os.remove("temp.txt")

def test_ping():
    res = port_scanner.scapy_ping("en.wikipedia.org")
    assert res

def test_http():
    sys.stdout = open('http_temp.txt', 'w')
    port_scanner.http_banner('en.wikipedia.org', 80)
    sys.stdout = sys.__stdout__
    output = open('http_temp.txt', 'r').read()
    assert "HTTP/1.1" in output
    os.remove('http_temp.txt')

def test_ftp():
    sys.stdout = open('temp.txt', 'w')
    port_scanner.generic_banner('ftp.cs.brown.edu', 21)
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    #Check if FTP successful connection code is in output
    assert "220" in output
    os.remove('temp.txt')

def test_bad_input():
    sys.stdout = open('temp.txt', 'w')
    port_scanner.main(["", "localhost", "asdasd", "1000"])
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Require an ip address, a start port, and a end port" in output
    os.remove('temp.txt')