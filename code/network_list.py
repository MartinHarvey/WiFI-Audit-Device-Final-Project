import subprocess
import sys

def main(output=None):
    #If path present, open file at that path
    if (output is not None):
        sys.stdout = open(output, 'w')
    #Run the process and save the stdout
    # "-f BSSID,SSID,CHAN,SIGNAL,SECURITY" filters output to those columns
    proc = subprocess.Popen(
        ["nmcli","-f", "BSSID,SSID,CHAN,SIGNAL,SECURITY" ,"dev", "wifi"], 
        stdout=subprocess.PIPE
        )
    #Take the stdout, read it and decode it from hex to string
    print(proc.stdout.read().decode())
    sys.stdout == sys.__stdout__

if __name__ == "__main__":
    #Grab a path if provided from the command line
    try:
        output = sys.argv[1]
    except:
        output = None
    
    main(output)