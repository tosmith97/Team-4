import json
from pydub import AudioSegment
from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
    jsonify,
    current_app,
    render_template
)
from flask_login import (
    current_user,
    login_required
)
import nexmo
import wave

from flask_rq import get_queue

from app import db

from app.calls.forms import CreateCallForm

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
    ncco_data['hostname'] = 'http://8978f380.ngrok.io' #current_app.config['HOST_NAME']
    conversation_uuid = request_data['conversation_uuid']
    query_string = {'conversation_uuid': conversation_uuid}
    encoded_query_string = '?' + urllib.parse.urlencode(query_string)
    ncco_data['conversation_uuid'] = encoded_query_string
    filein = open('NCCO/calls.json')
    src = Template(filein.read())
    filein.close()
    ncco = json.loads(src.substitute(ncco_data))
    print(request_data)
    print(ncco)
    sys.stdout.flush()

    # attack uuid to call db object
    initial_phone_number = request_data.get('from', None)
    print('number is %s' % initial_phone_number)
    if initial_phone_number:
        # get most recent call based on who called the number + hasn't been updated before + most recent
        last_call = db.session.query(Call).filter(Call.initial_phone_number == initial_phone_number, Call.call_uuid == None).order_by(Call.id.desc()).first()
        print('call num is %s' % last_call.initial_phone_number)
        if last_call:
            last_call.call_uuid = request_data.get('uuid', datetime.today().strftime('%Y-%m-%d'))
            db.session.commit()

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
        sys.stdout.flush()
        response = client.get_recording(url)
        uuid = res.get('recording_uuid', datetime.today().strftime('%Y-%m-%d'))
        fn = os.path.join(*[os.getcwd(), 'recordings', uuid + '.wav'])

        # get most recent call based on who called the number + hasn't been updated before + most recent
        last_call = db.session.query(Call).filter(Call.call_uuid == uuid).first()
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

@calls.route('/create-call', methods=['GET', 'POST'])
@login_required
def new_call():
    form = CreateCallForm()
    sys.stdout.flush()
    if form.validate_on_submit():
        call = Call(
            user=current_user.id,
            initial_phone_number=form.initial_phone_number.data,
            call_name=form.call_name.data,
            num_channels=form.num_callers.data,
            _phone_numbers=form.phone_numbers.data
        )
        db.session.add(call)
        db.session.commit()   
        sys.stdout.flush()
        return redirect(url_for('calls.call_status', call_title=form.call_name.data))
    
    return render_template('calls/new_call.html', form=form)


@calls.route('/create-call/new/<call_title>', methods=['GET', 'POST'])
@login_required
def call_status(call_title):
    return render_template('calls/call_status.html', call_title=call_title)