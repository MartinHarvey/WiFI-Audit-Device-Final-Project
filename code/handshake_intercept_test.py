import handshake_intercept
import sys
import subprocess

def test_iface():
    #Check if there is no monitor interface
    assert handshake_intercept.check_iface()
    #create a monitor iface
    handshake_intercept.create_iface()
    #Assert there is a monitor iface
    assert not handshake_intercept.check_iface()
    #set the channel to channel 5
    handshake_intercept.set_channel(5)
    #check the channel has been set to 5
    channel_check = subprocess.Popen(["iw", "dev"], stdout=subprocess.PIPE)
    assert b"channel 5" in channel_check.stdout.read()
    #remove the moninor iface
    handshake_intercept.remove_iface()
    #assert no monitor iface remains
    assert handshake_intercept.check_iface()

def test_no_input():
    sys.stdout = open('temp.txt', 'w')
    handshake_intercept.main()
    sys.stdout = sys.__stdout__
    output = open('temp.txt', 'r').read()
    assert "Need a output file and a wifi channel to listen on" in output
    os.remove('temp.txt')