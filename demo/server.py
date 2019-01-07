import socket
import sys
import cv2
import pickle
import numpy as np
import struct 
import psutil
import time
import pyshark
import os
import subprocess
import re
import datetime




HOST='localhost'
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('Socket created')

s.bind((HOST,PORT))
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')
print("server Program id ",os.getpid())
pid = os.getpid()

cmd = 'ps -p '+str(pid)+' -o %cpu'
os.system(cmd)
totalsum = 0.0 # to store cpu usage to get avg val
conn,addr=s.accept()

print('Addr ',addr)

start = time.time()
data = b''
payload_size = struct.calcsize("L") 
i= 0
avgTime = 0.0
frame_width = 720
frame_height = 337
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    out.write(frame) # writing to date file
    #print (frame)
    if frame is None:
        break
    
    if(i>0):
        newTime = datetime.datetime.now()
        avgTime += ((newTime - oldTime).total_seconds())
        oldTime = newTime
    else:
        oldTime = datetime.datetime.now()
    i+=1
    if(i % 20 ==0):
        print(i," frames done")
    val = subprocess.check_output(cmd, shell=True);
    strval =  val.decode('ASCII')
    strval = strval.replace('%CPU', '')
    totalsum+=float(strval)

    #cv2.imshow('frame',frame) #to show frae screen
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print("frames ",i)
os.system(cmd)
out.release()
print("Avg Cpu usage server ","%.2f" % round(totalsum/i,2))
print("Avg Interval Time ","%.5f" % round(avgTime/i,5), " secs")
end = time.time()
print(end - start)
