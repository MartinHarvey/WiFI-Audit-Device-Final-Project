import port_scanner
import os
import sys
import subprocess
# Tests require active internet connection. Uses online resources like en.wikipedia.org or the localhost
def test_localhost():
    #setup
    sys.stdout = open('temp.txt', 'w')
    port_scanner.main("localhost", "0", "1000")    
    sys.stdout = sys.__stdout__
    output = open("temp.txt", 'r').read()
    #assertions for tests
    assert "localhost is online" in output
    #teardown
    os.remove("temp.txt")

#Just pings wikipedia and sees what the output is
def test_ping():
    res = port_scanner.scapy_ping("en.wikipedia.org")
    assert res

#See if a successful HTTP response is gotten from an external website
def test_http():
    sys.stdout = open('http_temp.txt', 'w')
    port_scanner.http_banner('en.wikipedia.org', 80)
    sys.stdout = sys.__stdout__
    output = open('http_temp.txt', 'r').read()
    assert "HTTP/1.1" in output
    os.remove('http_temp.txt')

    sys.stdout = open('http_temp.txt', 'w')
    port_scanner.main('en.wikipedia.org', 80, 81)
    sys.stdout = sys.__stdout__
    output = open('http_temp.txt', 'r').read()
    assert "HTTP/1.1" in output
    os.remove('http_temp.txt')

#Check if a successful FTP response is recieved. generic banner is also
#used for SSH
def test_ftp():
    sys.stdout = open('temp.txt', 'w')
    port_scanner.generic_banner('ftp.cs.brown.edu', 21)
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    #Check if FTP successful connection code is in output
    assert "220" in output
    os.remove('temp.txt')

#Checks for error output on poor input
def test_bad_input():
    sys.stdout = open('temp.txt', 'w')
    port_scanner.main('localhost', "asdasd", 1000)
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Require an ip address, a start port, and a end port" in output
    os.remove('temp.txt')

def test_normal_scan():
    #setup
    sys.stdout = open('temp.txt', 'w')
    port_scanner.main("192.168.0.1", "0", "1000")    
    sys.stdout = sys.__stdout__
    output = open("temp.txt", 'r').read()
    #assertions for tests
    assert "192.168.0.1 is online" in output
    #teardown
    os.remove("temp.txt")


