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
import wave

from flask_rq import get_queue

from app import db

from app.models import User, Call
from string import Template
from flask import current_app
import uuid
import urllib
import os
import sys
from datetime import datetime
from io import BytesIO

import SpeechToTextServiceClient as STTS

calls = Blueprint('calls', __name__)


@calls.route('/ncco', methods=['GET', 'POST'])
def start_call():
    request_data = json.loads(request.data)
    ncco_data = {}
    ncco_data['hostname'] = 'b1233082.ngrok.io' #current_app.config['HOST_NAME']
    conversation_uuid = request_data['conversation_uuid']
    query_string = {'conversation_uuid': conversation_uuid}
    encoded_query_string = '?' + urllib.parse.urlencode(query_string)
    ncco_data['conversation_uuid'] = encoded_query_string
    filein = open('NCCO/calls.json')
    src = Template(filein.read())
    filein.close()
    ncco = json.loads(src.substitute(ncco_data))
    print(ncco)
    sys.stdout.flush()
    return jsonify(ncco)


@calls.route('/events', methods=['GET', 'POST'])
def call_events():
    print('events')
    res = json.loads(request.data)
    print(res)
    sys.stdout.flush()
    return "", 200

@calls.route('/recordings', methods=['GET', 'POST'])
def call_recordings():
    print("recordings")
    res = json.loads(request.data)
    client = nexmo.Client(
        application_id='4811d796-b14a-4775-b13c-4a93dec02e98',
        private_key='private.key',
    )
    url = res.get('recording_url')
    if url:
        print('we have url')
        print(url)
        response = client.get_recording(url)
        uuid = res.get('recording_uuid', datetime.today().strftime('%Y-%m-%d'))
        fn = os.path.join(*[os.getcwd(), 'recordings', uuid + '.wav'])

        # getting most recent is bad but for practical purposes works
        last_call = db.session.query((Call.call_uuid == None).order_by(Call.id.desc())).first()
        last_call.call_uuid = uuid
        last_call.filename = fn

        a = AudioSegment.from_file(BytesIO(response), channels=last_call.num_channels, sample_width=2, frame_rate=16000)
        a.export(fn, format="wav")
        db.session.commit()
        print('file saved')
        STTClient = STTS.SpeechToTextServiceClient()
        transcript = STTClient.transcribeAudioFile(fn, True)
        STTClient.saveTranscriptAsTxt(transcript, uuid)
    print()
    sys.stdout.flush()
    return "", 200

@calls.route('/create-call/new', methods=['GET', 'POST'])
def new_call():
    n_channels = request.n_channels
    call = Call(num_channels=n_channels)
    db.session.add(call)
    db.session.commit()
    print('called')
    return "", 200
