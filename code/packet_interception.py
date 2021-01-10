from scapy.all import sniff, wrpcap, conf
import subprocess
import sys

# make sure interface is up, and apply promiscuous permissions to it
def add_promiscuous(iface):
    subprocess.run(["ifconfig", iface, "up"])
    subprocess.run(["ifconfig", iface, "promisc"])

#gets given a single packet, appends it to a pcap file at the output path
def savepcap(packet, output_path):
    wrpcap(output_path, packet, append=True)

def main(args):
    try:
        iface = args[2]
    except IndexError:
        # If the user hasnt set a interface to listen on, just use the interface
        # scapy is using by default. 
        iface = conf.iface
    
    try: 
        output = args[1]
    except:
        print("Need a file to output packets to")
        exit(0)
    

    add_promiscuous(iface)
    sniff(filter='', prn=lambda p: savepcap(p, output), store=0)
main(sys.argv)