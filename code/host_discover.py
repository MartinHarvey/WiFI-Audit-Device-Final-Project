import socket
import os
import sys
from icmplib import ping

target = sys.argv[1]
print(ping(target).is_alive)

