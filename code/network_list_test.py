import network_list
import os
import mimetypes
import sys

def test_file_type():
    network_list.main(["", "temp.txt"])
    assert os.path.isfile('temp.txt')
    assert ('text/plain', None) == mimetypes.guess_type('temp.txt')
    os.remove('temp.txt')

def test_columns():
    sys.stdout = open('temp.txt', 'w')
    network_list.main([""])
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert output
    assert "SSID" in output
    assert "BSSID" in output
    assert "CHAN" in output
    assert "SIGNAL" in output
    assert "SECURITY" in output
    os.remove('temp.txt')
