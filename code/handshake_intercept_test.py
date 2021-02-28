import handshake_intercept
import sys

def test_iface():
    assert handshake_intercept.check_iface()
    handshake_intercept.create_iface()
    assert not handshake_intercept.check_iface()
    handshake_intercept.remove_iface()
    assert handshake_intercept.check_iface()
