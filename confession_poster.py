import json
import gspread
import Queue
import time
import sys
import socket
import facebook

print facebook.__file__

from datetime import datetime
from oauth2client.client import SignedJwtAssertionCredentials

#-----------------------
#MODIFY THE FOLLOWING VARS -> SHEET NAME, sleep amount, First Cell, columnToBeReadData, columnToBeReadTime, page id
#-----------------------

json_key = json.load(open('Name of json file acquired from google project manager'))
scope = ['Enter the scope of the sheet here, ex: https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope) 

gc = gspread.authorize(credentials)

wks = gc.open("Enter the google sheet name that you will be using, here").sheet1 #Sheet name 

cellNumber = 6  #First Cell to read

sleepamount = 30 #Interval between facebook posts

q = Queue.Queue()
#-------------------------

def Listener(): #Fetches confessions 
  #-----------------------
  #Variable declaration
  columnToBeReadData = 'B' #COLUMN WHERE CONFESSIONS ARE
  columnToBeReadTime = 'A' #COLUMN WHERE CONFESSIONS TIME ARE
  global cellNumber
  #-----------------------
  
  allNewPostRead = 0 #Do not change

  while (allNewPostRead == 0): #Read if there's unread confessions

    #Start at the first cell
    cellToBeReadData = columnToBeReadData + str(cellNumber) #Data
    cellToBeReadTime = columnToBeReadTime + str(cellNumber) #Time
    
    #------------------------- 
    #Flags, use for debugging purpose
    #print 'Currently Reading Cell - %s' %cellToBeReadData
    #print 'Currently Reading Cell - %s' %cellToBeReadTime

    #print 'Cell %s\'s (text) value - %s' %(cellToBeReadData,wks.acell(cellToBeReadData).value)
    #print 'Cell %s\'s (time) value - %s' %(cellToBeReadTime,wks.acell(cellToBeReadTime).value)
    #-------------------------

    if wks.acell(cellToBeReadTime).value  == '' or '': #If cell is empty
      print 'CELL IS EMPTY, it seems we read all' #We read all
      allNewPostRead = 1 #We read all
    else: 
      q.put((wks.acell(cellToBeReadData).value)) #Store confession in queue
      cellNumber += 1 #Next Confession
      #print 'Going to read cell A/B', cellNumber #Flag

def get_api(cfg): #No need to modify, this fetches auth, given CFG data

  graph = facebook.GraphAPI(cfg['access_token'])
  
  #-------------------------
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  #-------------------------
  
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  
  #-------------------------
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  #-------------------------

def main():

  global sleepamount

  cfg = {
    "page_id"      : "Enter the pages' id", 
    "access_token" : "Enter your access token here."
    }

  api = get_api(cfg)
  
  while True: #Listens and posts forever
    Listener()
    while q.empty() == 0:
      msg = q.get()
      status = api.put_wall_post(msg) #Post confession
    time.sleep(sleepamount)


if __name__ == "__main__":
  main()
