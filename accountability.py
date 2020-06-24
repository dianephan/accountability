import os
from flask import Flask, request, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime, date, time, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
RECIPIENT_NUMBER = os.environ.get('RECIPIENT_NUMBER')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

studentsDictionary = {}

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

def respond_list(status_list):
    #OPTIONAL function to 
    list_entries = "These are the people in your list: \n\n"
    for key, val in status_list.items():
        key_val = "\n" + key + ": " + val
        list_entries += key_val
    return(list_entries + str(status_list))

def help_text():
    return respond(f'Welcome to the Work Accountability Group!'
                + '\n Say "hello" to join the directory'
                + '\n Say "check" to view the directory'
                + '\n Respond with a number to change your status'
                + '\n 1 if you are studying'
                + '\n 2 if you are taking a break'
                + '\n 3 if you need a study buddy'
                + '\n 4 if you are done for the day'
                + '\n 5 if you are logging off')

def set_status(status, student):
    studentsDictionary[student] = status
    return respond(f'Your status has been changed to: ' + status)

@app.route('/webhook', methods=['POST'])
def webhook():
    student = request.form.get('From')
    message = request.form.get('Body').lower()

    if message == 'check':
        if studentsDictionary:
            return respond(studentsDictionary)
        else:
            return respond(f'No one is here. Invite people to your Work Accountability Group')
    if student in studentsDictionary and message == '1':
        status = 'Studying'
        return set_status(status, student)
    if student in studentsDictionary and message == '2':
        status = 'Taking a break'
        return set_status(status, student)
    if student in studentsDictionary and message == '3':
        status = 'Looking for a study buddy'
        return set_status(status, student)
    if student in studentsDictionary and message == '4':
        status = 'Done for the day'
        return set_status(status, student)
    if student in studentsDictionary and message == '5':
        status = 'Offline'
        return set_status(status, student)
    if message == 'hello' and student not in studentsDictionary:
        status = 'Online'
        studentsDictionary[student] = status
        return respond(f'Hello, {student}, you have been added to the directory')
    if message == 'hello' and student in studentsDictionary:
        status = 'Online'
        studentsDictionary[student] = status
        return respond(f'Welcome back, {student}!')
    else:
        return help_text()

@app.route('/breakcheck', methods=['GET'])
def getWebhook(): 
    #check: when was the last time your friend took a break 
    recipient_messages = client.messages.list(
                                # date_sent=datetime(2020, 6, 9),
                                date_sent = date.today(),
                                to=TWILIO_PHONE_NUMBER,
                                # limit=100
                            )
    recipient_break_list = []
    for msg in recipient_messages:
        if msg.body is '2':
            updated_time = msg.date_updated + timedelta(hours = -7)
            updated_time = str(updated_time)
            recipient_break_list.append(msg.from_ + ': took a break at ' + updated_time)
    return respond(f'{recipient_break_list}')

@app.route('/studycheck', methods=['GET'])
def getStudyStatus(): 
    #check: how many people have been studying? 
    recipient_messages = client.messages.list(
                            date_sent = date.today(),
                            to=TWILIO_PHONE_NUMBER,
                            # limit=100
                        )
    recipient_studied_list = []
    for msg in recipient_messages:
        # get entire history of those who said they were studying 
        if msg.body is '1':
            updated_time = msg.date_updated + timedelta(hours = -7)
            updated_time = str(updated_time)
            recipient_studied_list.append(msg.from_ + ': started studying at ' + updated_time)
    return respond(f'{recipient_studied_list}')
    
@app.route('/check', methods=['GET'])
def getCheckStatus(): 
    if studentsDictionary:
        return studentsDictionary
    else:
        return respond(f'No one is here. Invite people to your Work Accountability Group')

@app.route('/')
def hello_world():
    return respond(f'O hi I didnt expect you here')

