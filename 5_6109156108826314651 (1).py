from datetime import date, datetime
import json
from time import sleep
import requests
import os
import socket
from googleapiclient.discovery import build
from google.oauth2 import service_account
import threading
import socket
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID ='13KIbMLq2CqeHx8RfURtBf_KV9YKpIVkQO24JOttOq1k'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

#git
username = "aishwarya.gawande@innovaccer.com"
password = "eQ4amvIAygqZdxFkhsHS4435"



def clearSheet(sheetName):
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=sheetName+"!B4").execute()
    values = result.get('values', [])
    # Delete previous records
    request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=sheetName+"!B4:L15").execute()
    print("Cleared "+sheetName+" sheet")

def populateSheet(sheetName, lst1):
    # print(lst1)
    sleep(1)
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=sheetName+"!B4").execute()
    values = result.get('values', [])

    request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=sheetName+"!B4:L15", valueInputOption="USER_ENTERED",
                                                     insertDataOption="OVERWRITE", body={"values": lst1}).execute()
    print("Populated "+sheetName+" sheet")

def getBugsCreated(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Bug) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug) AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text) #deserialize data 
    total1 = var['total']
    # import pdb; pdb.set_trace() #breakpoint
    total=json.dumps(total1)  #serialize
    # import pdb; pdb.set_trace()
    print(url)
    print(total)
    return int(total)

def getBugsRejected(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Bug) AND (status = Rejected OR (status changed to Closed FROM Rejected) OR resolution in (Rejected, "Not a Bug", "Working as Expected", Duplicate, "Cannot Reproduce", "Won\'t Do", Declined, Deferred, "Deployment Issue", "Data Issue", "Infrastructure Issue", "As per Design", "Issue due to other module", "To Be Done via config tool", "Feature Obsolete")) AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug) AND (status = Rejected OR (status changed to Closed FROM Rejected) OR resolution in (Rejected, "Not a Bug", "Working as Expected", Duplicate, "Cannot Reproduce", "Won\'t Do", Declined, Deferred, "Deployment Issue", "Data Issue", "Infrastructure Issue", "As per Design", "Issue due to other module", "To Be Done via config tool", "Feature Obsolete")) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug) AND filter = "Engg Rejected Tickets" AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    #deserialize data 
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getBugsOpen(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Bug) AND priority in (Critical, High) AND resolution = Unresolved AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug) AND priority in (Critical, High) AND resolution = Unresolved AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug) AND resolution = Unresolved AND filter != "Engg Rejected Tickets" AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text) #deserialize data 
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSupportCreated(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Support) AND '+month
   #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Support) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Support) AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSupportRejected(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Support) AND (status = Rejected OR (status changed to Closed FROM Rejected) OR resolution in (Rejected, "Not a Bug", "Working as Expected", Duplicate, "Cannot Reproduce", "Won\'t Do", Declined, Deferred, "Deployment Issue", "Data Issue", "Infrastructure Issue", "As per Design", "Issue due to other module", "To Be Done via config tool", "Feature Obsolete")) AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Support) AND (status = Rejected OR (status changed to Closed FROM Rejected) OR resolution in (Rejected, "Not a Bug", "Working as Expected", Duplicate, "Cannot Reproduce", "Won\'t Do", Declined, Deferred, "Deployment Issue", "Data Issue", "Infrastructure Issue", "As per Design", "Issue due to other module", "To Be Done via config tool", "Feature Obsolete")) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Support) AND filter = "Engg Rejected Tickets" AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSupportOpen(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Support) AND priority in (Critical, High) AND resolution = Unresolved AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Support) AND priority in (Critical, High) AND resolution = Unresolved AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Support) AND resolution = Unresolved AND filter != "Engg Rejected Tickets"  AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSDTicketsCreated(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Bug, Support) AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSDRejected(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Bug, Support) AND (status = Rejected OR (status changed to Closed FROM Rejected) OR resolution in (Rejected, "Not a Bug", "Working as Expected", Duplicate, "Cannot Reproduce", "Won\'t Do", Declined, Deferred, "Deployment Issue", "Data Issue", "Infrastructure Issue", "As per Design", "Issue due to other module", "To Be Done via config tool", "Feature Obsolete")) AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND (status = Rejected OR (status changed to Closed FROM Rejected) OR resolution in (Rejected, "Not a Bug", "Working as Expected", Duplicate, "Cannot Reproduce", "Won\'t Do", Declined, Deferred, "Deployment Issue", "Data Issue", "Infrastructure Issue", "As per Design", "Issue due to other module", "To Be Done via config tool", "Feature Obsolete")) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND filter = "Engg Rejected Tickets" AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSDOpen(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder","Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND issuetype in (Bug, Support) AND priority in (Critical, High) AND resolution = Unresolved AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND priority in (Critical, High) AND resolution = Unresolved AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND resolution = Unresolved AND filter != "Engg Rejected Tickets" AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getSDBreach(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND priority in (Critical, High) AND issuetype in (Bug, Support) AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder", "Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND ("Time to resolution" =breached() OR "Time to first response" =breached()) AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND priority in (Critical, High) AND issuetype in (Bug, Support) AND "Product[Dropdown]" in ('+product+') AND ("Time to resolution" =breached() OR "Time to first response" =breached()) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND priority in (Critical, High) AND issuetype in (Bug, Support) AND "Product[Dropdown]" in ('+product+') AND ("Time to resolution" =breached() OR "Time to first response" =breached()) AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)

def getHighCriticalSDTickets(month,product):
    # url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND priority in (Critical, High) AND issuetype in (Bug, Support) AND "Product[Dropdown]" in (inref, Patient360,InNote,InCare,"Strategy Builder", "Payer Solution", "Contact Center", InConnect,"TeleMedicine Patient","TeleMedicine Provider", inreport,"Care Management - CBO/SDOH","CMS Payer Member Portal", "CMS Dev Portal","TeleMedicine Admin","Payer Registry", InOffice, "CMS 3rd Party Mobile App") AND ("Time to resolution" =breached() OR "Time to first response" =breached()) AND '+month
    #url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND priority in (Critical, High) AND '+month
    url = 'https://innovaccer.atlassian.net/rest/api/2/search?jql=project = SD AND "Product[Dropdown]" in ('+product+') AND issuetype in (Bug, Support) AND priority in (Critical, High) AND '+month
    result = requests.get(url, auth=(username, password))
    print("Status Code : "+str(result.status_code))
    var = json.loads(result.text)
    total1 = var['total']
    print(url)
    total=json.dumps(total1)
    print(total)
    return int(total)