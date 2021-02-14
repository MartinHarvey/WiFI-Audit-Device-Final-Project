import bluetooth
import sys


def main(args):
	try:
		sys.stdout = open(args[1], 'w')
		print(sys.argv[1])
	except IndexError:
		pass
	try:
		devices = bluetooth.discover_devices(lookup_names=True)
		print("Address           Name") 
		for addr, name in devices:
			print(addr + " " + name)
	except OSError:
		print("No bluetooth hardware to use")

if __name__ == "__main__":
	main(sys.argv)

