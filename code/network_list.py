import subprocess
import sys

def main(args):
    try:
        output = open(args[1], 'w')
    except IndexError:
        output = None
    subprocess.run(["nmcli","-f", "SSID,SIGNAL,SECURITY" ,"dev", "wifi"], stdout=output)

main(sys.argv)