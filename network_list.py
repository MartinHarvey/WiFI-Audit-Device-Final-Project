import subprocess

output = open("networks.txt", 'w')
subprocess.run(["nmcli","-f", "SSID,SIGNAL,SECURITY" ,"dev", "wifi"], stdout=output)