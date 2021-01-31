import bluetooth
import sys


def main(args):
    try:
        sys.stdout = open(sys.argv[1], 'w')
    except IndexError:
        pass
    try:
      	devices = bluetooth.discover_devices(lookup_names=True)
    except OSError:
      	print("No bluetooth hardware to use")

    print("Address           Name") 
    for addr, name in devices:
    	print(addr + " " + name)
	
    
if __name__ == "__main__":
    main(sys.argv)

