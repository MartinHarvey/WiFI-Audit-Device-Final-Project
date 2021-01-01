import bluetooth

try:
    print(bluetooth.discover_devices())
except OSError:
    print("No bluetooth hardware to use")

