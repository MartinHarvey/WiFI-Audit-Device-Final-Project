#!/usr/bin/python3
import socket
import sys
import ipaddress
import threading
import time
from scapy.all import IP, ICMP, sr, arping

def port_scan(target, start_port, end_port):
    ports_found = 0
    #iterate across every port between the start port and end port
    for port in range(start_port, (end_port+1)):
        scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_socket.settimeout(0.5)
        if(scan_socket.connect_ex((target, port)) == 0):
            ports_found += 1
            
            #Checking if port tends to host certain protocols
            try:
                port_type = socket.getservbyport(port, 'tcp')
                print("[!]Open Port - " + str(port) + "/TCP. Commonly used for " + port_type)
                if("http" in port_type and "https" not in port_type):
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
                #getservbyport returns an OSError exception if it doesnt recognise the port
                print("[!]Open Port - " + str(port) + "/TCP. This port is not standard for any common protocol")
        scan_socket.close()
    print("Total No of ports found: " + str(ports_found))

#Makes a GET request to the root directory of the website and parses/displays response
def http_banner(target, port):
    host = target + ":" + str(port)
    req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    req_socket.settimeout(3)
    req_socket.connect((target, port))
    req_socket.send(bytes("GET / HTTP/1.1\r\nHost: "+ host +" \r\n\r\n", "utf-8"))
    resp = req_socket.recv(4096)
    resp = resp.decode().split('\r\n')
    req_socket.close()
    for line in resp:
        print("|    " + line)

#Works for FTP and SSH so far. Just connects and waits for 4096 bytes of a response
def generic_banner(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((target, port))
    response = sock.recv(4096).decode()
    print("|    " + response)

#On test VM response is garbled but seems to be valid UTF-16
#Otherwise similar to generic_banner(). Other telnet services online return
#do not work with UTF-16. Going to use raw bytes for now
def telnet_banner(target, port):
    telnet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telnet_socket.settimeout(3)
    telnet_socket.connect((target, port))
    response = telnet_socket.recv(1024)
    print("|    " + str(response))

def scapy_ping(target):
    #scapy does not play nice with the loopback interface, so you cant
    #ping localhost/127.0.0.1 with scapy packets
    try:
        if(target == "127.0.0.1" or target == "localhost"):
            return True
    
        icmp_packet = IP(dst=target)/ICMP(id=101)
        succ, fail  = sr(icmp_packet, verbose=False, timeout=5)
        return (len(succ) == 1 and len(fail) == 0)
    except:
        return False


def ARP_ping(address):
    #scapy is not a fan of the loopback interface. localhost is always gonna be running, so 
    # so we just return the address in an array
    try: 
        if(address == "127.0.0.1" or address == "localhost"):
            return [address]

        #ping address, put recieved ARP response packets into response
        response, failed = arping(address, verbose=False)
        alive_hosts = []
        #iterate through the response packets and get the address and append to the alive_hosts
        #array. 
        for x in range(len(response)):
            alive_hosts.append(response[x][1].psrc)
        return alive_hosts
    except socket.gaierror:
        return []

def main(target=None, start_port=None, end_port=None, output_file=None): 
    start = time.time()
    #Get the file to redirect the output to if the user has supplied a path
    if(output_file is not None):
        sys.stdout = open(output_file, 'w')

    #Check if inputs are there. CHecks types too
    try:
        target  = str(target)
        start_port = int(start_port)
        end_port   = int(end_port)
    except:
        print("Require an ip address, a start port, and a end port")
        return 0
    #ARP_ping returns a array of alive addresses
    alive_hosts = ARP_ping(target)
    #If we get alive hosts back, run through the array. If not, try to ping the target
    if(len(alive_hosts)>0):
        for addr in alive_hosts:
            print(addr + " is online")
            port_scan(addr, start_port, end_port)
    else:
        if(scapy_ping(target)):
                print(target + " is online")
                port_scan(target, start_port, end_port)
    end = time.time()
    print("Time Taken " + str(end - start))

if __name__ == "__main__":
    #Get any input from command line
    try:
        target     = sys.argv[1]
        start_port = int(sys.argv[2])
        end_port   = int(sys.argv[3])
    except (IndexError, ValueError):
        print("Require an ip address, a start port, and a end port")
        exit()

    main(target, start_port, end_port)