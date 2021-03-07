import handshake_intercept
import sys
import subprocess

def test_iface():
    assert handshake_intercept.check_iface()
    handshake_intercept.create_iface()
    assert not handshake_intercept.check_iface()
    handshake_intercept.set_channel(5)
    channel_check = subprocess.Popen(["iw", "dev"], stdout=subprocess.PIPE)
    assert b"channel 5" in channel_check.stdout.read()
    handshake_intercept.remove_iface()
    assert handshake_intercept.check_iface()
