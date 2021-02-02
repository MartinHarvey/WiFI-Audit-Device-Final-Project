from scapy.all import *
import sys
import subprocess

def parse_packets(packet, output):
    if packet.haslayer(Dot11):
        wrpcap(output, packet, append=True)

def create_iface():
    subprocess.run(["iw", "phy0", "interface", "add", "mon0", "type", "monitor"])
    subprocess.run(["ifconfig", "mon0", "up"])

def set_channel(channel):
    subprocess.run(["iwconfig", "mon0", "channel", str(channel)])

def main(args):
    try:
        outpath = args[1]
        channel = args[2]
    except IndexError:
        print("Need a output file and a wifi channel to listen on")
        exit(0)
    
    proc = subprocess.Popen(["iw", "dev"], stdout=subprocess.PIPE)
    iw_results = proc.stdout.read()

    if(b"mon0" not in iw_results):
        create_iface()
    
    set_channel(channel)
    sniff(filter="tcp", prn=lambda p: parse_packets(p, outpath), store=0, iface='mon0')

if __name__ == "__main__":
    main(sys.argv)
