import json

import nexmo

from flask_rq import get_queue

from string import Template
import uuid
import urllib
import os
import sys
from datetime import datetime
from io import BytesIO

def start_call():
    request_data = {'from': '12622717345', 'conversation_uuid': 'uuid'}
    ncco_data = {}
    ncco_data['hostname'] = current_app.config['HOST_NAME']
    ncco_data['NEXMO_NUMBER'] = '12013657126'
    conversation_uuid = request_data['conversation_uuid']
    query_string = {'conversation_uuid': conversation_uuid}
    encoded_query_string = '?' + urllib.parse.urlencode(query_string)
    ncco_data['conversation_uuid'] = encoded_query_string
    filein = open('../../NCCO/calls.json')
    src = Template(filein.read())
    filein.close()

    # attach uuid to call db object
    initial_phone_number = request_data.get('from', None)

    if initial_phone_number:
        # get most recent call based on who called the number + hasn't been updated before + most recent
        last_call = {'num_channels': 3, '_phone_numbers': '12344324567;18655434856'}
        if last_call:
            ncco_data['num_channels'] = last_call['num_channels']
            ncco = json.loads(src.substitute(ncco_data))

            for number in last_call['_phone_numbers'].split(';'):
                ncco.append({'action': 'connect', 'eventUrl': ['https://' + ncco_data['hostname'] + '/calls/events'], 'from': ncco_data['NEXMO_NUMBER'], 'endpoint': [{'type': 'phone', 'number': number}]})
            return ncco
    return ncco


print(start_call())