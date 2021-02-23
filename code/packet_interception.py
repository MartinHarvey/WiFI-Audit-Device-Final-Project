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


def main(output, count_num=0, iface=None): 
    iface = conf.iface
    try: 
        count_num = int(count_num)
    except:
        count_num = 0

    add_promiscuous(iface)
    if(count_num > 0):
        sniff(
            prn=lambda p: wrpcap(output, p, append=True), 
            store=0, 
            count=count_num
            )
    else:
        sniff(
            prn=lambda p: wrpcap(output, p, append=True), 
            store=0
            )
    
    rem_promiscuous(iface)


if __name__ == "__main__":
    try: 
        output = sys.argv[1]
    except:
        print("Need a file to output packets tom, ")
        exit(0)

    try:
        count = sys.argv[2]
    except:
        count = 0
    try:
        iface = sys.argv[3]
    except:
        iface = None
    main(output, count, iface)
