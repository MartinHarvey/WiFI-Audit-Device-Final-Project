import network_dictionary_attack
import os
import pytest
import sys

#Check if the error output for no wordlist being given works.
def test_missing_input():
    sys.stdout = open('temp.txt', 'w')
    network_dictionary_attack.main("Network Name")
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Wordlist supplied not found" in output
    os.remove('temp.txt')

#Basically the same as test_missing_input but checks if the 
#error output is correct for a path being supplied, but the 
#path refers to a file that doesnt exist
def test_bad_list_path():
    sys.stdout = open('temp.txt', 'w')
    network_dictionary_attack.main("Network-Name", "This-file-doesnt-exist")
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Wordlist supplied not found" in output
    os.remove('temp.txt')