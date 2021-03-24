import time
import csv
import os
import glob
import mariadb
import sys
import datetime
import mysql.connector

def insert_varibles_into_table(timenow, oventemp, ambienttemp, tempdiff):
    try:
        connection = mysql.connector.connect(
	    host='localhost',
            database='solaroven',
            user='pythonscripting',
            password='12345')
        cursor = connection.cursor()
    except mysql.connector.Error as error: print("Failed")

base_dir = '/sys/bus/w1/devices'
internal_temp_file = base_dir + '/28-01204f1dcf61/w1_slave'
#second sensor path
ambient_temp_file = base_dir + '/28-01204f1dcf61/w1_slave'

def read_temp_internal():
    #To read the sensor data, just open the w1_slave file
    f = open(internal_temp_file, 'r')
    data = f.readlines()
    f.close()
    deg_f = ''
    if data[0].strip()[-3:] == 'YES':
        temp = data[1][data[1].find('t=')+2:]
        #If temp is 0 or not numeric an exception 
        #will occur so lets handle it gracefully
        try:
            if float(temp)==0:
                deg_f = 32
            else:
                deg_f = (float(temp)/1000)*9/5+32
        except:
            print("Error with t=", temp)
            pass
    return deg_f

def read_temp_ambient():
    #To read the sensor data, just open the w1_slave file
    f = open(ambient_temp_file, 'r')
    data = f.readlines()
    f.close()
    deg_f = ''
    if data[0].strip()[-3:] == 'YES':
        temp = data[1][data[1].find('t=')+2:]
        #If temp is 0 or not numeric an exception 
        #will occur so lets handle it gracefully
        try:
            if float(temp)==0:
                deg_f = 32
            else:
                deg_f = (float(temp)/1000)*9/5+32
        except:
            print("Error with t=", temp)
            pass
    return deg_f

while True:
    timenow = str(datetime.datetime.now())
    oventemp = str(read_temp_internal())
    ambienttemp = str(read_temp_ambient())
    tempdifference = read_temp_internal() - read_temp_ambient()
   # print(timenow, oventemp, ambienttemp, tempdifference)
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='solaroven',
            user='pythonscripting',
            password='12345')
        cursor = connection.cursor()
    except mysql.connector.Error as error: print("Failed")
    mySql_insert_query = """INSERT INTO data (Date, Oven_Temp, Ambient_Temp, Temp_Difference) 
                            VALUES (%s, %d, %d, %d) """
    record = (timenow, oventemp, ambienttemp, tempdifference)
    cursor.execute(mySql_insert_query, record)
    connection.commit()
