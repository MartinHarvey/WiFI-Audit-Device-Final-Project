from scapy.all import sniff, wrpcap, conf
import subprocess
import sys

# make sure interface is up, and apply promiscuous permissions to it
def add_promiscuous(iface):
    subprocess.run(["ifconfig", iface, "up"])
    subprocess.run(["ifconfig", iface, "promisc"])

def rem_promiscuous(iface):
    subprocess.run(["ifconfig", iface, "-promisc"])
#gets given a single packet, appends it to a pcap file at the output path
def savepcap(packet, output_path):
    wrpcap(output_path, packet, append=True)

def main(args):
    try:
        iface = args[3]
    except IndexError:
        # If the user hasnt set a interface to listen on, just use the interface
        # scapy is using by default. 
        iface = conf.iface
    try: 
        count_num = int(args[2])
    except IndexError:
        count_num = 0
    
    try: 
        output = args[1]
    except:
        print("Need a file to output packets to")
        exit(0)

    add_promiscuous(iface)
    if(count_num > 0):
        sniff(filter='', prn=lambda p: savepcap(p, output), store=0, count=count_num)

    else:
        sniff(filter='', prn=lambda p: savepcap(p, output), store=0)


if __name__ == "__main__":
    main(sys.argv)
