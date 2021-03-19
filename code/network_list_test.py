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
    sys.stdout = open("temp.txt", "w")
    network_list.main()
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "SSID" in output
    assert "BSSID" in output
    assert "CHAN" in output
    assert "SIGNAL" in output
    assert "SECURITY" in output
    os.remove('temp.txt')


