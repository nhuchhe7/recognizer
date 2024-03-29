# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# import os
# import psycopg2
# import cv2
# import numpy as np
# import re
# from datetime import datetime
# import mysql.connector



# # Get the relativ path to this file (we will use it later)
# FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# # * ---------- Create App --------- *
# app = Flask(__name__)
# CORS(app, support_credentials=True)


# def DATABASE_CONNECTION():
#     return mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="12345678",
#                 database="project"
#                 )



# mydb = DATABASE_CONNECTION()

# cur = mydb.cursor()
# date = datetime.today().strftime('%Y-%m-%d')
# print(date)
# sql = ("""SELECT MAX(time) FROM faceapp_attendancetb WHERE t_id='{}' AND date='{}'""".format('730320',date))
# print(sql)
# cur.execute(sql)
# time1=cur.fetchall()
# t=time1[0][0]
# print(type(t),t)




# * ---------- IMPORTS --------- *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import psycopg2
import cv2
import numpy as np
import re
from datetime import datetime
import mysql.connector
import psycopg2


# Get the relativ path to this file (we will use it later)
FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# * ---------- Create App --------- *
app = Flask(__name__)
CORS(app, support_credentials=True)


#
# * ---------- DATABASE CONFIG --------- *
# DATABASE_USER = os.environ['ROOT']
# DATABASE_PASSWORD = os.environ['12345678']
# DATABASE_HOST = os.environ['localhost']
# DATABASE_PORT = os.environ['3306']
# DATABASE_NAME = os.environ['project']

# def DATABASE_CONNECTION():
#     return mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="12345678",
#                 database="project"
#                 )


def DATABASE_CONNECTION():
    return psycopg2.connect(database="project", user="postgres", password="manish", host="127.0.0.1", port="5432")



def check(t1):
    # time_str = '13::55::26'
    # time_object = datetime.strptime(time_str, '%H::%M::%S').time()
    # print(type(time_object))
    # print(time_object)
    mydb = DATABASE_CONNECTION()
    # date = datetime.today().strftime('%Y-%m-%d')
    # print(date)
    # cur = mydb.cursor()
    # #sql = ("""SELECT MAX(time) FROM faceapp_attendancetb WHERE t_id='{}'""".format(code))
    # sql = ("""SELECT MAX(time) FROM faceapp_attendancetb WHERE t_id='{}' AND date='{}'""".format(code,date))
    # print(sql)
    # cur.execute(sql)
    if t1 is not None:
        t1 = datetime.strptime(str(t1),'%H:%M:%S.%f').time()
        t2 = datetime.now().time()
        interval=datetime.combine(datetime.today(), t2) - datetime.combine(datetime.today(), t1)
        print(interval)
        minutes = interval.total_seconds() / 60
        if minutes>0 and minutes<5:
            return 0
        else:
            return 1
    else:
        return 1



def get_late():
    mydb=DATABASE_CONNECTION()
    cur=mydb.cursor()
    sqll=("SELECT * FROM faceapp_timesetting WHERE id = 1 ")
    cur.execute(sqll)
    data=cur.fetchall()
    t1=intime=data[0][1]
    tolerance=data[0][3]
    t2=datetime.now().time()
    interval=datetime.combine(datetime.today(),t2) - datetime.combine(datetime.today(),t1)
    intt=interval.total_seconds()/60
    intt=int(intt)
    return(intt, tolerance)



# * --------------------  ROUTES ------------------- *
# * ---------- Get data from the face recognition ---------- *
@app.route('/receive_data', methods=['POST'])
def get_receive_data():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data['name'])
        u_id=json_data['name']
       
        mydb = DATABASE_CONNECTION()
        cur = mydb.cursor()
        print(mydb)


        # sql1 = ("SELECT code FROM faceapp_staffinfo WHERE name ='{}'".format(name))
        # print(sql1)

        # cur.execute(sql1)
        # code = cur.fetchall()
        # # code='730320'
        # print(code[0][0])
        # c=code[0][0]
        # datetime object containing current date and time
        time = datetime.now().time()
        date = datetime.today().strftime('%Y-%m-%d')
        # date = datetime.strptime(str(date), "%Y-%m-%d")
        c=u_id
        # sql = """SELECT MAX(time) FROM faceapp_attendancetb WHERE t_id='{}'""".format(c)
        sql = ("""SELECT MAX(time) FROM faceapp_attendancetb WHERE user_id='{}' AND date='{}'""".format(c,date))
        cur.execute(sql)
        time1=cur.fetchall()
        t=time1[0][0]
        print(type(t),t)
        if t is not None:
            sts=check(t)
            status='p'
            if sts==1:
                intt, tolerance=get_late()
                sql='''SELECT MAX(Id) AS LastID FROM faceapp_attendancetb'''
                cur.execute(sql)
                t_id=cur.fetchall()
                # print(t_id,type(t_id))
                idd=t_id[0][0]
                # print(idd,type(idd))
                if(intt>0 and intt<tolerance):
                    sql=('''INSERT INTO faceapp_attendancetb( id, date, time, user_id)VALUES ({},'{}','{}','{}') ''').format(idd+1,date,time,c)
                else:
                    sql=('''INSERT INTO faceapp_attendancetb( id, date, time,user_id, late_time)VALUES({},'{}','{}','{}','{}')'''.format(idd+1,date,time,c,intt))
                print(sql)
                cur.execute(sql)
                mydb.commit()
        else:
            ss='p'
            tt=5
            sql1 = ("SELECT * FROM faceapp_timesetting WHERE id=1")
            cur.execute(sql1)
            d= cur.fetchall()
            # print(d[0][0])
            t1=intime=d[0][1]
            tolerance=d[0][3]
            print(d)
            # t1 = datetime.strptime(str(intime),'%H:%M:%S.%f').time()
            t2 = datetime.now().time()
            interval=datetime.combine(datetime.today(), t2) - datetime.combine(datetime.today(), t1)
            print(interval,type(interval))
            print(tolerance)
            # tolerance=datetime.strptime(str(tolerance),'%H:%M:%S.%f').time()
            # tolerance=tolerance.total_seconds()/60
            intt = interval.total_seconds()/60
            print(type(intt))
            sql='''SELECT MAX(Id) AS LastID FROM faceapp_attendancetb'''
            cur.execute(sql)
            t_id=cur.fetchall()
            # print(t_id,type(t_id))
            idd=t_id[0][0]
            # print(idd,type(idd))
            intt=int(intt)
            if(intt>0 and intt<tolerance):
                sql=('''INSERT INTO faceapp_attendancetb( id,date, time, user_id)VALUES({},'{}','{}','{}','{}')'''.format(intt+1,date,time,c))
            else:
                sql=('''INSERT INTO faceapp_attendancetb( date, time, user_id, late_time)VALUES({},'{}','{}','{}','{}')'''.format(intt+1,date,time,c,intt))
            cur.execute(sql)
            mydb.commit()


    return jsonify(json_data)






#        
                                 
# * -------------------- RUN SERVER -------------------- *
if __name__ == '__main__':
    # * --- DEBUG MODE: --- *
    app.run(host='127.0.0.1', port=5000, debug=True)
    #  * --- DOCKER PRODUCTION MODE: --- *
    # app.run(host='0.0.0.0', port=os.environ['PORT']) -> DOCKER
