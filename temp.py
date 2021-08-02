from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import psycopg2
import cv2
import numpy as np
import re
from datetime import datetime
import mysql.connector

def DATABASE_CONNECTION():
    return mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345678",
                database="project"
                )



mydb = DATABASE_CONNECTION()

cur = mydb.cursor()
date = datetime.today().strftime('%Y-%m-%d')
print(date)
sql = ("""SELECT MAX(time) FROM faceapp_attendancetb WHERE t_id='{}' AND date='{}'""".format('730320',date))
print(sql)
cur.execute(sql)
time1=cur.fetchall()
t=time1[0][0]
print(type(t),t)
