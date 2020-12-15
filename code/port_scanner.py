import socket
import sys
import ipaddress
from icmplib import ping

def port_scan(target, start_port, end_port):
    ports_found = 0
    #iterate across every port between the start port and end port
    for port in range(start_port, (end_port+1)):
        scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scan_socket.settimeout(5)
        if(scan_socket.connect_ex((target, port)) == 0):
            ports_found += 1
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
    print("Total No of ports found: " + str(ports_found))

#Makes a GET request to the root directory of the website and displays
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

#Works for FTP and SSH so far. Just connects and waits for 4096 bytes of a response
def generic_banner(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target, port))
    response = sock.recv(4096).decode()
    print(response)

#On test VM response is garbled but seems to be valid UTF-16
#Otherwise similar to generic_banner()
def telnet_banner(target, port):
    telnet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telnet_socket.connect((target, port))
    response = telnet_socket.recv(1096)
    print(response)


def main(args): 
    try:
        target = sys.argv[1]
        start_port = int(args[2])
        end_port   = int(args[3])
    except IndexError:
        print("Require an ip address, a start port, and a end port")
        exit()
    # CIDR_hosts holds all the possible addresses in a CIDR block inputted by the user. If the
    # CIRD_hosts is empty, then the input (target) is a single IP address 
    CIDR_hosts = list(ipaddress.ip_network(target).hosts())
    if(CIDR_hosts != []):
        for addr in CIDR_hosts:
            addr = str(addr)
            # Check if host is online by pinging it and run a port scan if so
            if(ping(addr).is_alive):
                print(addr + " is online")
                port_scan(addr, start_port, end_port)
    else:
        if(ping(target).is_alive):
                print(target + " is online")
                port_scan(target, start_port, end_port)
main(sys.argv)