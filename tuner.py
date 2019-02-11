import subprocess
import time
import re

from gateway import CiscoRouterGateway

gateway_address = "http://192.168.1.1"
router_username = ''
router_password = ''
timeout_sec     = 120
num_speedtest   = 5

router = CiscoRouterGateway(
	address=gateway_address, 
	username=router_username,
	password=router_password
)

for channel in range(1, 11):
	router.set_channel(channel)
	time.sleep(timeout_sec)

	print("Speeds at channel:" + str(channel))
	values = []
	for j in range(num_speedtest):
		download_speed = subprocess.Popen('speedtest-cli --no-upload | grep "Download:"', shell=True, stdout=subprocess.PIPE).stdout.read()
		download_speed_val = re.findall("Download: (.*) Mbit/s", download_speed)[0]
		print(download_speed_val + " Mbit/s")
		values.append(float(download_speed_val))
	print("Average download speed:" + str(sum(values) / len(values)) + " MBit/s")
