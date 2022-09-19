from scapy.all import *
import pandas as pd
import numpy as np
from datetime import datetime
import time
from threading import Thread
import subprocess, shlex, time
import threading

import pandas as pd
from mac_vendor_lookup import MacLookup


import asyncio
from websockets import connect
import time
#Run monitor_mode.sh first
#To get RSSI values we need the macaddress and channel frequency of the connection of the device we are attempting to 
#sniff

class RSSI_Scanner:

    def __init__(self, mac_address, ws_uri):
        self.ws = None
        self.mac_address = mac_address

        self.channel_c = 11
        self.change_freq_channel(self.channel_c)        

        t = AsyncSniffer(iface="wlan1", prn=self.method_filter_HTTP, store=0)
        t.daemon = True
        t.start()

        t = Thread(target=self.start_ws, args=(ws_uri,))
        t.daemon = True
        t.start()

        #for channel_c in range(1,3):
        
        
        
        # t = Thread(target=self.change_freq_channel, args=(self.channel_c,))
        # t.daemon = True        
        # t.start()

    def start_ws(self):
        asyncio.run(self.connect_ws("ws://localhost:8765"))

    async def connect_ws(self, ws_uri):
        self.ws = await connect(ws_uri)

    def change_freq_channel(self, channel_c):
        print('Changing to Channel ', str(channel_c))
        command = 'sudo iwconfig wlan1 channel ' + str(channel_c)
        command = shlex.split(command)
        subprocess.Popen(command, shell=False) 
        

    def method_filter_HTTP(self, pkt):
        missed_count = 0 #Number of missed packets while attempting to write to file
        
        cur_dict = {}
        cur_dict['mac_1'] = pkt.addr1
        cur_dict['mac_2'] = pkt.addr2
        cur_dict['rssi'] = pkt.dBm_AntSignal

        #if cur_dict['mac_1'] == router_mac:
        if cur_dict['mac_2'] == self.mac_address:

            print("pkit", pkt.show)
            # file_object = open('rssi.txt', 'a')
            print(cur_dict)
            
            try:
                
                to_write = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")) + " " + cur_dict['mac_1'] + "," + cur_dict['mac_2'] + "," + str(cur_dict['rssi']) + "\n"
                rssi = cur_dict['rssi']
                if self.ws != None:
                    self.ws.send(rssi)
                # file_object.write(to_write)
                # file_object.close()
                
            except Exception as e:
                
                print("E\t", e, missed_count)
                missed_count += 1

        #print('emd')
        
        #return 0

#raspberrypi8 mac address
RSSI_Scanner(mac_address="b8:27:eb:fc:23:5e", ws_uri="ws://localhost:8001")
