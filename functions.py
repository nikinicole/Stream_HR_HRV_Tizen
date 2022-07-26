# -*- coding: utf-8 -*-
"""


"""
#import time
import json
import socket
import logging
#import sqlite3
import asyncio
#import websockets
#import matplotlib.pyplot as plt
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import pandas as pd


PPG = []
hr = []
hrv = []
HR = []
HRV = []
timestamp = []
timestamp_hr = []

my_sw = []

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")


STATE = {"value": -127, "name": ""}

USERS = set()
WATCHES = set()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip




def state_event():
    return json.dumps({"type": "state", **STATE})

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    logging.info("New User...")
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    logging.info("User gone...")
    await notify_users()



async def w_register(websocket):
    WATCHES.add(websocket)
    logging.info("New watch connected...")

async def w_unregister(websocket):
    WATCHES.remove(websocket)
    logging.info("Watch gone...")
    
    



async def watch(websocket, path):
   
  
   
    await w_register(websocket)
    

    try:
                

        async for message in websocket:

            if message == "quit":
                break

            var = ''
            try:
               
                var = json.loads(message) #Messaggio ricevuto dal galaxy
                print(var)
               
            except ValueError:
                print("Decoding JSON has failed")

            if "type" in var:

                if var["type"] == "quit":
                    break

                   
                if var["type"] == "hrm":
                    hr  = float(var["hr"])
                    hrv = float(var["hrv"])
                    
                    print('HRV ARRIVA: ' + str(hrv))
                    time_hr = float(var["timestamp"])
                    HRV.append(hrv)
                    HR.append(hr)
                    timestamp_hr.append(time_hr)
                    
                                       
    finally:
        
     
        
       
        #SAVE DATA TO CSV
        # filename is hrv_timestamp_.csv
        filename_hrv = 'hrv_' + dt_string + '.csv'
        my_df_hrv = pd.DataFrame()
        my_df_hrv['hrv'] = HRV
        my_df_hrv['hr'] =  HR
        
        my_df_hrv['timestamp'] = timestamp_hr
        print(my_df_hrv.head())
        my_df_hrv.to_csv(filename_hrv, sep = ';', header = True)
        
        
        
        
