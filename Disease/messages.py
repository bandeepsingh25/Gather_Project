from djongo.database import connect
import datetime
import time
import numpy as np
from twilio.rest import Client
import os

def menu(*args):
    return "Reply with the following numbers:\n 1: Check Symptoms. \n 2: Cases in your location \n 3: Main Menu"


def cases(collection, body):
    zipcode = int(body['FromZip'])
    number = collection.find( {'zipcode': {'$gt': zipcode - 3, '$lt': zipcode + 3}} ).count()

    return 'There are {} cases near your area'.format( number )


def give_symptom(collection, reply, mongo_db=None):
    phone = reply['From']
    body = reply['Body']

    try:
        collection.find_one_and_update( {'phone': phone}, {'$set': {'last_msg': body}},
                                        sort=[('last_msg_time', -1)] )
        return "Do you have Fever?"
    except:

        if collection['fever'] == None:
            mongo_db.find_and_modify( {'phone': phone}, {'$set': {'fever': body, 'last_msg': body}},
                                      sort=[('last_msg_time', -1)] )
            return "Days of Fever?"

        elif collection['days'] == None:
            mongo_db.find_and_modify( {'phone': phone}, {'$set': {'days': body, 'last_msg': body}},
                                      sort=[('last_msg_time', -1)] )
            return "Do You have a headache?"

        elif collection['headache'] == None:
            mongo_db.find_and_modify( {'phone': phone}, {'$set': {'headache': body, 'last_msg': body}},
                                      sort=[('last_msg_time', -1)] )
            return 'Send Yes to see your result'

        elif body == 'Yes':
            mongo_db.find_and_modify( {'phone': phone}, {'$set': {'menu_option': None, 'last_msg': body}},
                                      sort=[('last_msg_time', -1)] )

            chances = np.random.rand()*100

            account = os.environ['account']
            auth_token = os.environ['auth_token']
            client = Client( account, auth_token )

            if chances > 55:


                for numbers in [os.environ['Emergency_No_1'],os.environ['Emergency_No_2']]:
                    message = client.messages.create(
                        body="IMPORTANT: Potential Dengue outbreak in your region. Take preventive actions. Go to www.gather.com",
                        from_='+19845381103',
                        to=numbers)
            return ('There is a %.2f%% chance you have dengue'%chances)
        else:
            return "Invalid argument."


def response(msg):
    client = connect()
    database = client['gather-djongo-db']

    message = database.messages

    record = message.find( {'phone': msg['From']} ).sort( 'last_msg_time', -1 )

    if record.count() == 0:
        message.insert_one( {'phone': msg['From'], 'last_msg_time': datetime.datetime.now(),
                             'last_msg': None, 'menu_option': None, 'zipcode': int(msg['FromZip']),
                             'fever': None, 'days': None, 'headache': None} )

        return "Thanks for reaching out. \n" + menu()

    elif (time.mktime( datetime.datetime.now().timetuple() ) - time.mktime(
            record[0]['last_msg_time'].timetuple() )) / 60 > 5:
        message.insert_one( {'phone': msg['From'], 'last_msg_time': datetime.datetime.now(),
                             'last_msg': None, 'menu_option': None, 'zipcode': int(msg['FromZip']),
                             'fever': None, 'days': None, 'headache': None} )

       
        return menu()

    else:

        if record[0]['menu_option'] != '1':
            if msg['Body'] in ['1', '2', '3']:
                message.find_one_and_update( {'phone': msg['From']}, {'$set': {'menu_option': msg['Body']}},
                                             sort=[('last_msg_time', -1)] )

                return menu_functions[msg['Body']]( message, msg )


    if record[0]['menu_option'] == '1' and record[0]['last_msg'] != None:
        return give_symptom( record[0], msg, message )


menu_functions = {'1': give_symptom, '2': cases, '3': menu}


