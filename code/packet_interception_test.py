import packet_interception
import os
import sys
import subprocess
import mimetypes
from scapy.all import conf

#Uses MIME to check if we have a pcap file output
def test_file():
    packet_interception.main('temp.pcap', 5)
    assert os.path.isfile("temp.pcap")
    assert ('application/vnd.tcpdump.pcap', None) == mimetypes.guess_type('temp.pcap')
    os.remove('temp.pcap')

#Adds and removes promiscous perms from scapy default interface and then runs 
#ifconfig each time to see if the perms show ups as part of the output
def test_promisc():
    test_iface = conf.iface
    packet_interception.add_promiscuous(test_iface)
    proc = subprocess.Popen(["ifconfig", test_iface], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    assert b"PROMISC" in output
    packet_interception.rem_promiscuous(test_iface)
    proc = subprocess.Popen(["ifconfig", test_iface], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    assert b"PROMISC" not in output



