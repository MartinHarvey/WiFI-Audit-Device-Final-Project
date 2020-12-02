import socket
import os
import sys
import argparse
from icmplib import ping

def port_scan(args):
    try:
        target     = args[1]
        start_port = int(args[2])
        end_port   = int(args[3])
    except IndexError:
        print("Require an ip address, a start port, and a end port")
        exit()
    
    for port in range(start_port, end_port):
        scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_socket.settimeout(5)
        if(scan_socket.connect_ex((target, port)) == 0):
            try:
                port_type = socket.getservbyport(port, 'tcp')
                print("[!]Open Port - " + str(port) + "/TCP. Commonly used for " + port_type)
                if("http" in port_type):
                    print("[*]Banner grabbing over HTTP")
                    http_banner(target, port)
                if("ftp" in port_type):
                    print("[*]Banner grabbing over FTP")
                    generic_banner(target, port)
                if("telnet" in port_type):
                    print("[*]Banner grabbing over telnet")
                    telnet_banner(target, port)
                if("ssh" in port_type):
                    print("[*]Banner grabbing over SSH")
                    generic_banner(target, port)
            except OSError:
                print("[!]Open Port - " + str(port) + "/TCP. This port is not standard for any common protocol")
        scan_socket.close()

def http_banner(target, port):
    host = target + ":" + str(port)
    req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    req_socket.connect((target, port))
    req_socket.send(bytes("GET / HTTP/1.1\r\nHost: "+ host +" \r\n\r\n", "utf-8"))
    resp = req_socket.recv(4096)
    resp = resp.decode().split('\r\n')
    req_socket.close()
    for line in resp:
        print(line)

def generic_banner(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target, port))
    response = sock.recv(4096).decode()
    print(response)

def telnet_banner(target, port):
    telnet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telnet_socket.connect((target, port))
    response = telnet_socket.recv(4096).decode("UTF-16")
    print(response)


def main(args): 
    target = sys.argv[1]
    if(ping(target)):
        print("Host online")
        
        port_scan(args)
    else:
        print("Host not responding")
        exit()

main(sys.argv)