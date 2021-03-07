import network_list
import os
import mimetypes
import sys
import subprocess

# CHecking if the output file is a text file. Quick MIME test
def test_file_type():
    network_list.main("temp.txt")
    assert os.path.isfile('temp.txt')
    assert ('text/plain', None) == mimetypes.guess_type('temp.txt')
    os.remove('temp.txt')

#Check if the basic output is present when a network is detected
def test_columns():
    network_list.main('temp.txt')
    output = open('temp.txt', 'r').read()
    assert "SSID" in output
    assert "BSSID" in output
    assert "CHAN" in output
    assert "SIGNAL" in output
    assert "SECURITY" in output
    os.remove('temp.txt')

#Test that the feature runs from the command line
#Similar test in bluetooth_list_test
def test_cli():
    subprocess.run(["sudo", "python3", "network_list.py", "out.txt"])
    assert os.path.isfile('out.txt')
    output = open('out.txt', 'r').read()
    os.remove('out.txt')

