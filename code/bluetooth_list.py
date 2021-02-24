import bluetooth
import sys


def main(output=None):
	#Open file if path present
	if (output is not None):
		sys.stdout = open(output, 'w')
	
	try:
		#Run lookup function from bluetooth library and display results
		devices = bluetooth.discover_devices(lookup_names=True)
		print("Address           Name") 
		for addr, name in devices:
			print(addr + " " + name)
	except OSError:
		#OSError if no BT hardware available
		print("No bluetooth hardware to use")

if __name__ == "__main__":
	#Get path if there from command line
	try:
		output = sys.argv[1]
	except IndexError:
		output = None
	main(output)

