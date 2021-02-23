import bluetooth_list
import os
import sys
import mimetypes

def test_column():
    sys.stdout = open('temp.txt', 'w')
    bluetooth_list.main()
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Address           Name" in output
    os.remove('temp.txt')

def test_file_type():
    bluetooth_list.main("temp.txt")
    assert os.path.isfile('temp.txt')
    assert ('text/plain', None) == mimetypes.guess_type('temp.txt')
    os.remove('temp.txt')
