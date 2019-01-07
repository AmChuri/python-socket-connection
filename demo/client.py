import cv2
import numpy as np
import socket
import sys
import pickle
import struct 
import psutil
import time
import os
import subprocess
import re

start = time.time()


cap=cv2.VideoCapture("output.mp4")
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print("length ",frame_width )
print("width ",frame_height )
print("height ",length )
print("Client Program id ",os.getpid())
pid = os.getpid()
cmd = 'ps -p '+str(pid)+' -o %cpu'
os.system(cmd)
totalsum = 0.0 # to store cpu usage to get avg val
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))
i = 0 #framecount
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data))+data)

    if frame is None:
        break
    i+=1
    val = subprocess.check_output(cmd, shell=True);
    strval =  val.decode('ASCII')
    strval = strval.replace('%CPU', '')
    totalsum+=float(strval)
print("frames ",i)
os.system(cmd)
print("Avg Cpu usage client ","%.2f" % round(totalsum/i,2))

end = time.time()
print(end - start)
