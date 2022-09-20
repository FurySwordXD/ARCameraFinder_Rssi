import csv
from datetime import datetime
from scapy.all import *
import subprocess, shlex
from threading import Thread
import threading

import asyncio
from websockets import connect
import time


class RSSI_Scanner:
        '''
        Run monitor_mode.sh first to set up the network adapter to monitor mode.
        To get RSSI values, we need the MAC Address and Channel Frequency of the connection 
        of the device sending the packets.
        '''
        def __init__(self, mac_address, ws_uri):
                self.ws = None
                self.ws_uri = ws_uri
                self.mac_address = mac_address

                self.channel_c = 100
                self.change_freq_channel(self.channel_c) 
                self.file_name = 'rssi.csv' 
                self.create_rssi_file()     

                t = AsyncSniffer(iface="wlan1", prn=self.method_filter_HTTP, store=0)
                t.daemon = True
                t.start()

                t = Thread(target=self.start_ws)
                t.daemon = True
                t.start()

        def start_ws(self):
                asyncio.run(self.connect_ws())

        async def connect_ws(self):
                self.ws = await connect(self.ws_uri)

        def create_rssi_file(self):
                """Create and prepare a file for RSSI values"""
                header = ['date', 'time', 'dest', 'src', 'rssi']
                with open(self.file_name, 'w', encoding='UTF8') as f:
                        writer = csv.writer(f)
                        writer.writerow(header)

        def change_freq_channel(self, channel_c):
                """Change the channel network adapter listens on"""
                print('Changing to Channel ', str(channel_c))
                command = 'sudo iwconfig wlan1 channel ' + str(channel_c)
                command = shlex.split(command)
                subprocess.Popen(command, shell=False) 

        def method_filter_HTTP(self, pkt):
                """Save packet addresses and rssi values to file if mac address matches"""
                missed_count = 0 #Number of missed packets while attempting to write to file

                cur_dict = {}
                cur_dict['mac_1'] = pkt.addr1
                cur_dict['mac_2'] = pkt.addr2
                cur_dict['rssi'] = pkt.dBm_AntSignal

                if cur_dict['mac_2'] == DEV_MAC:
                        try:
                                date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f").split(",")
                                date = date_time[0]
                                time = date_time[1]

                                data = [date, time, cur_dict['mac_1'], cur_dict['mac_2'], cur_dict['rssi']]
                                with open(self.file_name, 'a', encoding='UTF8') as f:
                                        writer = csv.writer(f)
                                        writer.writerow(data)
                                        
                                rssi = cur_dict['rssi']
                                if self.ws != None:
                                        self.ws.send(rssi)

                                print(cur_dict)

                        except Exception as e:

                                print("E\t", e, missed_count)
                                missed_count += 1    


if __name__ == "__main__":
        DEV_MAC = "dc:a6:32:33:ae:15"
        rssi_scanner = RSSI_Scanner(mac_address=DEV_MAC, ws_uri="ws://10.193.187.236:8001")
        
        while True:
                pass
        

