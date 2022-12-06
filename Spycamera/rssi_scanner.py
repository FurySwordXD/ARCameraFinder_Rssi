import csv
from datetime import datetime
from scapy.all import *
import subprocess, shlex

class RSSIScanner:
	'''
	Run monitor_mode.sh first to set up the network adapter to monitor mode.
	To get RSSI values, we need the MAC Address and Channel Frequency of the connection 
	of the device sending the packets.
	'''
	def __init__(self, mac_address, channel, iface = "wlan1"):
		self.ws = None		
		self.mac_address = mac_address
		self.rssi = None

		self.channel_c = channel
		self.setup_adapter(self.channel_c)

		t = AsyncSniffer(iface=iface, prn=self.method_filter_HTTP, store=0)
		t.daemon = True
		t.start()		

	def get_rssi(self):
		rssi = self.rssi
		self.rssi = None
		return rssi

	def setup_adapter(self, channel_c):
		"""Setup and change the channel network adapter listens on"""
		commands = [
			"sudo ip link set wlan1 down", 
			"sudo iw dev wlan1 set type monitor", 
			"sudo ip link set wlan1 up", 
			"iw dev",
			f"sudo iwconfig wlan1 channel {channel_c}"
		]
		for command in commands:
			command = shlex.split(command)
			subprocess.Popen(command, shell=False)		

	def method_filter_HTTP(self, pkt):
		"""Save packet addresses and rssi values to file if mac address matches"""
		missed_count = 0 #Number of missed packets while attempting to write to file
		
		print(pkt.show())
		cur_dict = {}
		cur_dict['mac_1'] = pkt.addr1
		cur_dict['mac_2'] = pkt.addr2
		cur_dict['rssi'] = pkt.dBm_AntSignal

		if cur_dict['mac_2'] == self.mac_address:
			try:
				date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f").split(",")
				date = date_time[0]
				time = date_time[1]
				
				rssi = cur_dict['rssi']
				self.rssi = rssi
				print(cur_dict)

			except Exception as e:
				print("E\t", e, missed_count)
				missed_count += 1    


if __name__ == "__main__":	
	RSSIScanner(mac_address="dc:a6:32:33:ae:15", channel=100, iface="wlan1")