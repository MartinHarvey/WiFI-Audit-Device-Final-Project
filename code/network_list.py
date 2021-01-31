import subprocess
import sys

def main(args):
    try:
        output = open(args[1], 'w')
    except IndexError:
        output = None
    subprocess.run(["nmcli","-f", "BSSID,SSID,SIGNAL,SECURITY" ,"dev", "wifi"], stdout=output)

if __name__ == "__main__":
    main(sys.argv)