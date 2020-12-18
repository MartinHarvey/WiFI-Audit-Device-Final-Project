from scapy.all import sniff, wrpcap

def savepcap(packet):
    wrpcap('output.pcap', packet, append=True)

sniff(filter='icmp', prn=lambda packet: savepcap(packet), store=0)