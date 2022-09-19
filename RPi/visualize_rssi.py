import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

file_name = "rssi.csv"
df = pd.read_csv(file_name)
df['time'] = pd.to_datetime(df['time']) #convert time column to datetime objects
#print(df.head()) #shows first 5 rows in the data frame

fig, ax = plt.subplots()

ax.set_title('RSSI vs. Time')
ax.set_ylabel('RSSI (dbm)')
ax.set_xlabel('Time (min)')

minute_second_formatter = mdates.DateFormatter("%M:%S.%f")
ax.xaxis.set_major_formatter(minute_second_formatter)
fig.autofmt_xdate()

x = df['time']
y = df['rssi']

ax.plot_date(x,y)

'''
Excercise 1: Find the maximum rssi value in the dataframe and 
mark it using a different color in the plot
'''
#Remove before sending
max = df[df.rssi == df.rssi.max()]
ax.annotate('o',xy=(max['time'],max['rssi']), color='red') #change point with max rssi value to red

plt.show()


'''
Excercise 2: Can you think of a better way to find the point where the Pis
where closest together? We can remove outliers to filter out 'bad' RSSI values
and still find the location of our pi camera, but what are the implications of 
doing that? Implement your solution below.
'''