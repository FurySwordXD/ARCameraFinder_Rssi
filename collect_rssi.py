from scapy.all import *
import pandas as pd
import numpy as np
from datetime import datetime
import time
from threading import Thread
import subprocess,shlex,time
import threading

import csv
import os
import copy
import math
import pandas as pd
from mac_vendor_lookup import MacLookup

#Run monitor_mode.sh first
#To get RSSI values we need the macaddress and channel frequency of the connection of the device we are attempting to 
#sniff

locky = threading.Lock()

def Change_Freq_channel(channel_c):
    print('Changing to Channel ', str(channel_c))
    command = 'sudo iwconfig wlan1 channel ' + str(channel_c)
    command = shlex.split(command)
    subprocess.Popen(command, shell=False) 

dev_mac = "b8:27:eb:fc:23:5e" #raspberrypi8 mac address

#Prepares text file for RSSI Values
filename = 'rssi.txt'
file_object = open('rssi.txt', 'w')
file_object.close()

#missed_count = 0 


def method_filter_HTTP(pkt):
    missed_count = 0 #Number of missed packets while attempting to write to file
    
    cur_dict = {}
    cur_dict['mac_1'] = pkt.addr1
    cur_dict['mac_2'] = pkt.addr2
    cur_dict['rssi'] = pkt.dBm_AntSignal

    #if cur_dict['mac_1'] == router_mac:
    if cur_dict['mac_2'] == dev_mac:

        print("pkit", pkt.show)
        file_object = open('rssi.txt', 'a')
        print(cur_dict)
        
        try:
            
            to_write = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")) + " " + cur_dict['mac_1'] + "," + cur_dict['mac_2'] + "," + str(cur_dict['rssi']) + "\n"
            file_object.write(to_write)
            file_object.close()
            
        except Exception as e:
            
            print("E\t", e, missed_count)
            missed_count += 1

    #print('emd')
    
    #return 0

#for channel_c in range(1,3):
channel_c = 11
#print("Channel\t",channel_c)
t = Thread(target=Change_Freq_channel,args=(channel_c,))
t.daemon = True
locky.acquire()
t.start()
t = AsyncSniffer(iface="wlan1",prn=method_filter_HTTP,store=0)
t.start()
time.sleep(40)
t.stop()
locky.release()


'''
rssiFile = open("./rssi.txt")
rssiData = rssiFile.read()

dflist=[]
for rssi in rssiData.splitlines():
    d1 = {}
    spl = rssi.split(" ")
    print(spl)
    ost = spl[2].split(",")
    print(ost)
    d1['date'] = spl[0]
    d1['time'] = spl[1]

    d1['dst'] = ost[0]
    d1['src'] = ost[1]
    d1['rssi'] = ost[2]
    print(d1)
    dflist.append(d1)

df = pd.DataFrame(dflist)
print(df)
df.to_csv('rssi_mod.csv',index=False)
    # break


'''
# from datetime import datetime


'''
def merge(vioData, rssiData):
    
    mergedData = []
    print(rssiData)
    unqs = np.unique(rssiData['src'].values)
    print(unqs)

    dt_obj = pd.to_datetime('2013-01-01 09:10:12', format='%Y-%m-%d %H:%M:%S')
    rssiData['dt_obj'] =  pd.to_datetime(rssiData['time'], format='%H:%M:%S.%f')

    print(rssiData.head())

    # njt = vioData['date and time']
    vioData['time'] = vioData['date and time'].str.split(' ').str[1]
    # print(vioData)
    # ()+1

    vioData['dt_obj'] =  pd.to_datetime(vioData['time'], format='%H:%M:%S')

    print(vioData)

    dfnew = pd.merge_asof(rssiData, vioData, on='dt_obj')
    del dfnew['date and time']
    print(dfnew)
    return dfnew
'''
'''           
def interpolate(avgRssi):
    points = []
    data = []
    neededPoints = []
    for i in range(len(avgRssi)):
        for j in range(len(avgRssi[0])):
            if avgRssi[i][j] == -60:
                neededPoints.append((i,j))
            else:
                data.append(avgRssi[i][j])
                points.append((i,j))
    for (x,y) in neededPoints:
        outputValue = float(griddata(points=points,values=data, xi=(x,y), method="linear"))
        avgRssi[x][y] = outputValue
    return avgRssi

colnames=['date and time', 'x location', 'y location', 'z location'] 

vioData= pd.read_csv('./vioData.csv',names=colnames,skiprows=1)

print(vioData)
# ()+1
'''
'''
rssiData= pd.read_csv('rssi_mod.csv')
mergedData = merge(vioData, rssiData)

print(mergedData)


unqs = np.unique(mergedData['src'].values)
print(unqs)
dflist=[]
new_dict={}
new_dict['Camera Type']='origin'

new_dict['X Location']=0
new_dict['Y Location']=0
new_dict['Z Location']=0
new_dict['X Rotation']=0.0
new_dict['Y Rotation']=0.0
new_dict['Z Rotation']=0.0
new_dict['Image File']='camera'
dflist.append(new_dict)


for eval in unqs:
    df1 = mergedData[mergedData['src'] == eval]
    # print(eval,"\n",df1)
    x = np.array(df1['x location'].values)
    y = np.array(df1['y location'].values)
    rssi = np.array(df1['rssi'].values.astype(float))

    lowrow = (df1[df1.rssi == df1.rssi.max()]).to_dict(orient='records')[0]
    # print(lowrow)
    xval = lowrow['x location']
    yval = lowrow['y location']
    lowrow['name']=MacLookup().lookup(eval)
    try:

        print(MacLookup().lookup(eval))
    except Exception as e:
        print(e)
    print(eval,xval,yval, lowrow['rssi'])
    new_dict={}
    # ,X Location,Y Location,Z Location,X Rotation,Y Rotation,Z Rotation,Image File
    
    # new_dict['Camera Type']=lowrow['name']
    new_dict['Camera Type']='apple'

    new_dict['X Location']=lowrow['x location']
    new_dict['Y Location']=lowrow['y location']
    new_dict['Z Location']=lowrow['z location']
    new_dict['X Rotation']=0.0
    new_dict['Y Rotation']=0.0
    new_dict['Z Rotation']=0.0
    new_dict['Image File']='camera'



    dflist.append(new_dict)


    print(new_dict)
    # d1['x ocation']
# file = open('deviceinfo.csv', 'w')
# # file.write('Camera Type,X Location,Y Location,Z Location,X Rotation,Y Rotation,Z Rotation,Image File \n Device 1, ' + str(maxXValue) + ',' + str(print(maxVal, maxXValue, maxYValue)
# ) + '1.14138,0,0,0,camera');
# file.close()



df = pd.DataFrame(dflist)
df.to_csv("deviceinfo.csv",index=False)
'''
