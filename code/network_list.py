import subprocess
import sys

def main(output=None):
    if (output is not None):
        sys.stdout = open(output, 'w')
    proc = subprocess.Popen(["nmcli","-f", "BSSID,SSID,CHAN,SIGNAL,SECURITY" ,"dev", "wifi"], stdout=subprocess.PIPE)
    print(proc.stdout.read().decode())

if __name__ == "__main__":
    try:
        output = sys.argv[1]
    except:
        output = None
    
    main(output)