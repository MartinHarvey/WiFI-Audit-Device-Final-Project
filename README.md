# WiFi Audit Device
Software portion of final degree project carried out by Martin Harvey. The objective of the project was to build a small, cheap and easy to use device to assist in the auditing of the security of a conventional wifi network. Modules can be run either via the GUI or individually via the command line. 

Functions are:
* Host Discovery and Port Scanning
* Promiscuous Packet Interception
* List Local WiFi Networks
* List Local Bluetooth devices
* WiFi Network Dictionary Attack
* WPA Handshake Interception


## Installation
Dependencies are required for certain functions to operate

Python Libraries:

* Scapy
* wireless
* PyBluez


Linux Programs:
* nmcli (and by extension NetworkManager)
* airmon-ng (installed as part of aircrack-ng package)

The physical device is a Raspberry Pi 3 B+ with a touchscreen and using the nexmon drivers, but the software can, in theory, be run on any device running a recent Linux distribution. Even if your device does not support monitor mode (required for handshake interception), other features will work.

## Operation

Can be run via:
```bash
sudo python3 code/main_window.py
```

Or each individual module can be run on the cli independently. For example:
```
sudo python3 port_scanner.py <address/block> <start port> <end port> <output file (optional)>
```

## Testing
Unit tests have been written for pytest. pytest can be run with the following command. 
```
sudo python3 -m pytest 
```

## Disclaimer
This program should only be used on a network you have express permission to use it on. Using this program to commit any crime is strictly forbidden and I do not take any responsibility for the use of this program for illegal actions. 