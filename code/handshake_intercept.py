from scapy.all import *
import sys
import subprocess

def parse_packets(packet, output):
    pass

def main(args):
    pass
    try:
        outpath     = args[1]
        sniff_iface = args[2]
    except IndexError:
        print("Need a output file and a wifi interface")
        exit(0)

    filter_str = "tcp and host not " + str(get_if_addr(sniff_iface))
    sniff(filter=filter_str, prn=lambda p: parse_packets(p, outpath), store=0, iface=sniff_iface)

if __name__ == "__main__":
    main(sys.argv)