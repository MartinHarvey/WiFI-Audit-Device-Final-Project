from scapy.all import sniff, wrpcap
import sys
import subprocess

#Returns true if there are no 'mon' interface on the device. 'iw dev' lists
#wifi interfaces, and we can read and check if mon is in the results
def check_iface():
    proc = subprocess.Popen(["iw", "dev"], stdout=subprocess.PIPE)
    iw_results = proc.stdout.read()

    return (b"mon" not in iw_results)

#airmon-ng allows you to create a monitor interface
def create_iface():
    #'airmon-ng check kill' will check for any processes that can 
    #interfere with the monitor interface and kills them
    subprocess.run(["airmon-ng", "check", "kill"])
    #airmon-ng start wlan0 creates a monitor interface on the wlan0 interface
    #wlan0 is the default wifi interface on most devices (ie Raspberry Pi)
    subprocess.run(["airmon-ng", "start", "wlan0"])
    #Makes sure the monitor interface is actually up and running
    subprocess.run(["ifconfig", "wlan0mon", "up"])

def remove_iface():
    #Stops monitor mode running on wlan0
    subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"])
    subprocess.run(["sudo", "NetworkManager"])

#Need to set the interface to listen on a specific channel
def set_channel(channel):
    subprocess.run(["iwconfig", "wlan0mon", "channel", str(channel)])

def main(outpath, channel):
    #Some type checking.
    try:
        outpath = str(outpath)
        channel = int(channel)
    except TypeError:
        print("Need a output file and a wifi channel to listen on")
        return 0
    
    #If no mon interface, create one
    if(check_iface()):
        create_iface()
    
    #set channel to user supplied value
    set_channel(channel)
    try:
        #sniff for frames on the wlan0mon interface
        #filter defines a BPF filter for just capturing 802.11 Auth frames
        #and EAPOL key material frames
        #BPF filters are very fast. Way quicker than capturing every frame and use scapy to check
        #if they have certain layers/frame types. 
        #prn is the callback thats run on capturing a frame. Saves it to the user_supplied file
        sniff(
            iface='wlan0mon',
            filter="ether proto 0x888e or wlan type mgt subtype auth", 
            prn= lambda packet: wrpcap(outpath, packet, append=True)
            )
    except OSError:
        print("No wireless device exists")
        return 0

if __name__ == "__main__":
    try:
        outpath = sys.argv[1]
        channel = sys.argv[2]
    except IndexError:
        print("Need a output file and a wifi channel to listen on")
        exit(0)

    main(outpath, channel)
