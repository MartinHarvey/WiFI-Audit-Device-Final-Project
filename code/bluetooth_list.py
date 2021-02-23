import bluetooth
import sys


def main(output=None):
	if (output is not None):
		sys.stdout = open(output, 'w')
	
	try:
		devices = bluetooth.discover_devices(lookup_names=True)
		print("Address           Name") 
		for addr, name in devices:
			print(addr + " " + name)
	except OSError:
		print("No bluetooth hardware to use")

if __name__ == "__main__":
	try:
		output = sys.argv[1]
	except IndexError:
		output = None
	main(output)

