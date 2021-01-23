import packet_interception
import os
import sys
import subprocess
import mimetypes

def test_file():
    packet_interception.main(["", "temp.pcap", "5"])
    assert os.path.isfile("temp.pcap")
    assert ('application/vnd.tcpdump.pcap', None) == mimetypes.guess_type('temp.pcap')
    os.remove('temp.pcap')

def test_promisc():
    packet_interception.add_promiscuous("eth0")
    proc = subprocess.Popen(["ifconfig", "eth0"], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    assert b"PROMISC" in output
