import json
import urllib.request
import pprint
import mysql.connector
from datetime import datetime
from mysql.connector import Error


with open('config.json') as config_file:
        config = json.load(config_file) 
def loadJson(url):
  data = urllib.request.urlopen(url).read().decode()
  obj = json.loads(data)
  return obj;

streamingUrlList=[]
def getTotalResults():
   obj = loadJson("https://web-api-pepper.horizon.tv/oesp/v2/NL/nld/web/channels")
   total_channels=obj['totalResults']
   return total_channels


def getTotalStreamingURLS():
       obj = loadJson("https://web-api-pepper.horizon.tv/oesp/v2/NL/nld/web/channels")
       for channel in obj['channels']:
              for station in channel['stationSchedules']:
                     keys=list(station.values())[0]
                     for videostream in keys['videoStreams']:
                         streamingUrlList.append(videostream['streamingUrl'])
       return len(streamingUrlList)
      
def connectToDB(host,user,password,database):
       conn= None
       try:
           conn= mysql.connector.connect(host=host,user=user,password=password,database=database)

       except Error as e:
          print("Error while connecting to MySQL", e)
       return conn



def insertData():
       try:
          con=connectToDB(config["db_host"],config["db_username"],config["db_password"],config["db_name"])
          if (con==None):
                 print("Failed to connect to DB")
          else:
             cursor=con.cursor()
             total_channels=getTotalResults()
             total_streaming_urls=getTotalStreamingURLS()
             execution_time=datetime.now()
             sql = "INSERT INTO monitoring_logs ( total_channels, total_streaming_urls, execution_time) VALUES (%s, %s, %s)"
             val = (total_channels,total_streaming_urls,execution_time)
             cursor.execute ( sql, val )
             print("1 row inserted")
             con.commit()
       except Error as e:
          print("Error while excution of query in MySQL", e)
       finally:
               if con.is_connected():
                   cursor.close()
                   con.close()
                   print("MySQL connection is closed")

insertData()
