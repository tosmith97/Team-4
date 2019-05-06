import json
from pydub import AudioSegment
from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
    jsonify,
    current_app
)
import nexmo

from flask_rq import get_queue

from app import db

from app.models import User
from string import Template
from flask import current_app
import uuid
import urllib
import os
from datetime import datetime

calls = Blueprint('calls', __name__)


@calls.route('/ncco', methods=['GET', 'POST'])
def start_call():
    request_data = json.loads(request.data)
    ncco_data = {}
    ncco_data['hostname'] = '127.0.0.1:5000' #current_app.config['HOST_NAME']
    conversation_uuid = request_data['conversation_uuid']
    query_string = {'conversation_uuid': conversation_uuid}
    encoded_query_string = '?' + urllib.parse.urlencode(query_string)
    ncco_data['conversation_uuid'] = encoded_query_string
    filein = open('NCCO/calls.json')
    src = Template(filein.read())
    filein.close()
    ncco = json.loads(src.substitute(ncco_data))
    print(jsonify(ncco))
    return jsonify(ncco)


@calls.route('/events', methods=['GET', 'POST'])
def call_events():
    print('events')
    res = json.loads(request.data)
    client = nexmo.Client(
        application_id='4811d796-b14a-4775-b13c-4a93dec02e98',
        private_key='private.key',
    )
    url = res.get('recording_url')
    if url:
        print('we have url')
        response = client.get_recording(url)        
        fn = os.path.join(*[os.getcwd(), 'recordings', res.get('recording_uuid', datetime.today().strftime('%Y-%m-%d')) + '.wav'])
        with open(fn, "wb+") as f:
            f.write(response)
        a = AudioSegment.from_file(fn).resample(sample_width=16)
        a.export(fn, format="wav")
        print('file saved')
    print()
    return "", 200

@calls.route('/recordings', methods=['GET', 'POST'])
def call_recordings():
    print(request.data)
    print("RECORDING")
    return "", 200

@calls.route('/create-call/new', methods=['GET', 'POST'])
def new_call():
    print('called')
    return "", 200
