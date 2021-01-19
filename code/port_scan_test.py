import port_scanner
import os
import sys

# Tests require active internet connection. Uses online resources like en.wikipedia.org or the localhost
def test_localhost():
    #setup
    sys.stdout = open('temp.txt', 'w')
    port_scanner.main(["", "localhost", "0", "1000"])    
    sys.stdout = sys.__stdout__
    output = open("temp.txt", 'r').read()
    #assertions for tests
    assert "localhost is online" in output
    assert "No of ports found" in output
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
    port_scanner.generic_banner('speedtest.tele2.net', 21)
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "220 (vsFTPd" in output
    os.remove('temp.txt')