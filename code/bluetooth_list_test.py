import bluetooth_list
import os
import sys
import mimetypes
import subprocess

#Test if the default columns are printed out. 
#Used to check if the most basic output is displayed after 
#checking for local devices. Even if no devices are present, 
#this will pass. 
def test_column():
    sys.stdout = open('temp.txt', 'w')
    bluetooth_list.main()
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Address           Name" in output
    os.remove('temp.txt')

#Easy check of MIME type of an output file
def test_file_type():
    bluetooth_list.main("temp.txt")
    assert os.path.isfile('temp.txt')
    assert ('text/plain', None) == mimetypes.guess_type('temp.txt')
    os.remove('temp.txt')

#Test that the feature runs from the command line
#Run it like you would from the cli and check that a output file is created
def test_cli():
    subprocess.run(["sudo", "python3", "bluetooth_list.py", "out.txt"])
    assert os.path.isfile('out.txt')
    os.remove('out.txt')


