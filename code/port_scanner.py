#!/usr/bin/python3
import socket
import sys
import ipaddress
import threading
import time
from scapy.all import IP, ICMP, sr

def port_scan(target, start_port, end_port):
    ports_found = 0
    #iterate across every port between the start port and end port
    for port in range(start_port, (end_port+1)):
        scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_socket.settimeout(2)
        if(scan_socket.connect_ex((target, port)) == 0):
            ports_found += 1
            
            #CHecking if port tends to host certain protocols
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
    req_socket.settimeout(20)
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
    sock.connect((target, port))
    response = sock.recv(4096).decode()
    print("|    " + response)

#On test VM response is garbled but seems to be valid UTF-16
#Otherwise similar to generic_banner(). Other telnet services online return
#do not work with UTF-16. Going to use raw bytes for now
def telnet_banner(target, port):
    telnet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telnet_socket.connect((target, port))
    response = telnet_socket.recv(1024)
    print("|    " + str(response))

def scapy_ping(target):
    #scapy does not play nice with the loopback interface, so you cant
    #ping localhost/127.0.0.1 with scapy packets
    if(target == "127.0.0.1" or target == "localhost"):
        return True
    
    icmp_packet = IP(dst=target)/ICMP()
    succ, fail  = sr(icmp_packet, verbose=False, timeout=5)
    return (len(succ) == 1 and len(fail) == 0)

def main(args): 
    start = time.time()
    try:
        target = args[1]
        start_port = int(args[2])
        end_port   = int(args[3])
    except (IndexError, ValueError):
        print("Require an ip address, a start port, and a end port")
        return 0
    #Get the file to redirect the output to if the user has supplied a path
    try:
        output_file = args[4]
        sys.stdout = open(output_file, 'w')
    except IndexError:
        #stdout will already be normal stdout, so no need to do anything
        pass
    # CIDR_hosts holds all the possible addresses in a CIDR block inputted by the user. If the
    # CIDR_hosts is empty, then the input (target) is a single IP address 
    try:
        CIDR_hosts = list(ipaddress.ip_network(target).hosts())
    except ValueError:
        #ip_network will raise a ValueError if target isnt a IPv4 or IPv6 address. This means user can still input 
        #host names or URLs etc
        CIDR_hosts = []
    if(CIDR_hosts != []):
        for addr in CIDR_hosts:
            #Each address in CIDR_hosts is not stored as a string, and since we need to use strings, we convert
            addr = str(addr)
            # Check if host is online by pinging it and run a port scan if so
            if(scapy_ping(addr)):
                print(addr + " is online")
                #Extra code that can make the program wait for the last port scan to finish
                #before beginning the next port scan on the new host. Unsure if it makes any
                #difference, so its currently commmented out. More research required
                try:
                    scan_thread.join()
                except:
                    pass
                #Create a new thread to run the port scan in the background
                scan_thread = threading.Thread(target=port_scan, args=(addr, start_port, end_port,))
                scan_thread.start()
    else:
        if(scapy_ping(target)):
                print(target + " is online")
                port_scan(target, start_port, end_port)
    end = time.time()
    print("Time Taken " + str(end - start))

if __name__ == "__main__":
    main(sys.argv)