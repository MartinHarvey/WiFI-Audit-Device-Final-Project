import bluetooth_list
import os
import sys

def column_test():
    bluetooth_list.main(["", "temp.txt"])
    output = open('temp.txt', 'r').read()
    assert "Address           Name" in output
    os.remove('temp.txt')

