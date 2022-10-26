import urllib.request
import json
import socket
import datetime
import time
import configparser
import mysql.connector
from mysql.connector import Error

socket.setdefaulttimeout(30)

#connect to config file to collect IP, SQL server and login data later
config=configparser.ConfigParser()
config.read('config.ini')

#construct target URL
url = 'http://' + config.get('ENVOY', 'IP')+'/production.json'

#connect to Envoy and collect data
try:
        response = urllib.request.urlopen(url,  timeout=30)
        string = response.read().decode('utf-8')
        data = json.loads(string)
        wNow = str(data['production'][0]['wNow'])
        readTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['production'][0]['readingTime']))
#        print(readTime)
except urllib.error.URLError as error:
#        print('Data was not retrieved because error: {}\nURL: {}'.format(error.reason, url) )
        quit()  # exit the script - some error happened
except socket.timeout:
#        print('Connection to {} timed out, '.format( url))
        quit()  # exit the script - cannot connect
        
        response.close

#connect to Mysql and put data in
try:
    connection = mysql.connector.connect(host = config.get('SERVER', 'host'),
                                         database=config.get('SERVER', 'database'),
                                         user=config.get('LOGIN', 'user'),
                                         password=config.get('LOGIN', 'password'))
    if connection.is_connected():
        db_Info = connection.get_server_info()
#        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
 #       print("You're connected to datase: ", record)
        #find last DB entry and check if data is new (based on datetime). If not new, end.
        cursor.execute("SELECT currentDateTime FROM Production ORDER BY id DESC LIMIT 1;")
        latest = cursor.fetchone()
        lastTime = latest[0]
        checkTime = lastTime.strftime("%Y-%m-%d %H:%M:%S")
        if checkTime == readTime:
           print("duplicate")
           quit()
        else:
            mySql_insert_query = """INSERT INTO Production (currentDateTime, wnow) values (%s, %s)"""
            record = (readTime, wNow)
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            print("successfully inserted")
except Error as e:
    quit()
#    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
#        print("MySQL connection is closed")
        
quit()
