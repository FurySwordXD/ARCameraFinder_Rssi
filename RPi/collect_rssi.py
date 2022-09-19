import csv
from datetime import datetime
from scapy.all import *
import subprocess, shlex
import threading
from threading import Thread

'''
Run monitor_mode.sh first to set up the network adapter to monitor mode.
To get RSSI values, we need the MAC Address and Channel Frequency of the connection 
of the device sending the packets.
'''

# DEV_MAC = "b8:27:eb:fc:23:5e" #raspberrypi8 mac address
DEV_MAC = "dc:a6:32:33:ae:15" #raspberrypi15 mac address
CHANNEL_NUM = 5 #Channel to listen on
IFACE = "wlan1" #Interface for sniffer
DURATION = 40 #Number of seconds to sniff for
file_name = 'rssi.csv'

def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    header = ['date', 'time', 'dest', 'src', 'rssi']
    with open(file_name, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def change_freq_channel(channel_num):
    """Change the channel network adapter listens on"""
    print('Changing to Channel ', str(channel_num))
    command = 'sudo iwconfig wlan1 channel ' + str(channel_num)
    command = shlex.split(command)
    subprocess.Popen(command, shell=False) 

def method_filter_HTTP(pkt):
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
            with open(file_name, 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            
            print(cur_dict)
            
        except Exception as e:

            print("E\t", e, missed_count)
            missed_count += 1    
    

if __name__ == "__main__":
    create_rssi_file()

    lock = threading.Lock()

    print("Channel\t", CHANNEL_NUM)
    t = Thread(target = change_freq_channel, args = (CHANNEL_NUM,))
    t.daemon = True
    t.acquire()
    t.start()

    t = AsyncSniffer(iface = IFACE, prn = method_filter_HTTP, store = 0)
    t.start()
    time.sleep(DURATION)
    t.stop()
    
    lock.release()

