import subprocess
import sys

def main(args):
    try:
        output = open(args[1], 'w')
        sys.stdout = output
    except IndexError:
        output = None
    proc = subprocess.Popen(["nmcli","-f", "BSSID,SSID,CHAN,SIGNAL,SECURITY" ,"dev", "wifi"], stdout=subprocess.PIPE)
    print(proc.stdout.read().decode())

if __name__ == "__main__":
    main(sys.argv)