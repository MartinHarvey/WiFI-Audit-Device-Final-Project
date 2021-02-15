from scapy.all import *
from scapy.contrib import *
import sys
import subprocess

def parse_packets(packet, output):
    if packet.haslayer(Dot11Auth) or packet.haslayer(EAPOL):
        wrpcap(output, packet, append=True)

def check_iface():
    proc = subprocess.Popen(["iw", "dev"], stdout=subprocess.PIPE)
    iw_results = proc.stdout.read()

    return (b"mon" not in iw_results)

def create_iface():
    subprocess.run(["airmon-ng", "check", "kill"])
    subprocess.run(["airmon-ng", "start", "wlan0"])
    subprocess.run(["ifconfig", "wlan0mon", "up"])

def set_channel(channel):
    subprocess.run(["iwconfig", "wlan0mon", "channel", str(channel)])

def main(args):
    try:
        outpath = args[1]
        channel = args[2]
    except IndexError:
        print("Need a output file and a wifi channel to listen on")
        exit(0)
    
    if(check_iface()):
        create_iface()
    
    set_channel(channel)
    print("Now beginning to sniff")
    try:
        packets = sniff(iface='wlan0mon', filter="ether proto 0x888e or wlan type mgt subtype auth", prn= lambda packet: wrpcap(output, packet, append=True))
        print(packets)
    except OSError:
        print("No device exists")
        return 0

if __name__ == "__main__":
    main(sys.argv)
