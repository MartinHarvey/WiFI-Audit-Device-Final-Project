import bluetooth_list
import os
import sys

def test_column():
    sys.stdout = open('temp.txt', 'w')
    bluetooth_list.main([""])
    output = open('temp.txt', 'r').read()
    sys.stdout = sys.__stdout__
    assert "Address           Name" in output
    os.remove('temp.txt')

