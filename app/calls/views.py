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
from app.helpers.pdfs import PDFEngine

calls = Blueprint('calls', __name__)


@calls.route('/ncco', methods=['GET', 'POST'])
def start_call():
    request_data = json.loads(request.data)
    ncco_data = {}
    ncco_data['hostname'] = current_app.config['HOST_NAME']
    ncco_data['NEXMO_NUMBER'] = '12013657126'
    conversation_uuid = request_data['conversation_uuid']
    query_string = {'conversation_uuid': conversation_uuid}
    encoded_query_string = '?' + urllib.parse.urlencode(query_string)
    ncco_data['conversation_uuid'] = encoded_query_string
    filein = open('NCCO/calls.json')
    src = Template(filein.read())
    filein.close()
    print(request_data)

    # attach uuid to call db object
    initial_phone_number = request_data.get('from', None)
    print('number is %s' % initial_phone_number)
    if initial_phone_number:
        # get most recent call based on who called the number + hasn't been updated before + most recent
        last_call = db.session.query(Call).filter(Call.initial_phone_number == initial_phone_number).order_by(Call.id.desc()).first()
        print('call num is %s' % last_call.initial_phone_number)
        if last_call:
            ncco_data['num_channels'] = last_call.num_channels
            ncco = json.loads(src.substitute(ncco_data))
            last_call.call_uuid = request_data.get('conversation_uuid', datetime.today().strftime('%Y-%m-%d'))
            db.session.commit()

        for number in last_call._phone_numbers.split(';'):
            ncco.append({'action': 'connect', 'eventUrl': ['https://' + ncco_data['hostname'] + '/calls/events'], 'from': ncco_data['NEXMO_NUMBER'], 'endpoint': [{'type': 'phone', 'number': number}]})
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
        sys.stdout.flush()
        response = client.get_recording(url)
        uuid = res.get('conversation_uuid', datetime.today().strftime('%Y-%m-%d'))
        fn = os.path.join(*[os.getcwd(), 'recordings', uuid + '.wav'])

        # get most recent call based on who called the number + hasn't been updated before + most recent
        last_call = db.session.query(Call).filter(Call.call_uuid == uuid).first()
        last_call.filename = fn

        a = AudioSegment.from_file(BytesIO(response), channels=last_call.num_channels, sample_width=2, frame_rate=16000)
        a.export(fn, format="wav")
        print('file saved')
        STTClient = STTS.SpeechToTextServiceClient()
        transcript = STTClient.transcribeAudioFile(fn, True)
        STTClient.saveTranscriptAsTxt(transcript, uuid)

        participants = [last_call.initial_phone_number]
        participants.extend(last_call._phone_numbers.split(';'))
        pdf_engine = PDFEngine(participants=participants, text=transcript)
        pdf_engine.textPDF()
        print('texted PDF')
        last_call.pdf_link = pdf_engine.pdf_url
        db.session.commit()

    print()
    sys.stdout.flush()
    return "", 200

@calls.route('/create-call', methods=['GET', 'POST'])
@login_required
def new_call():
    form = CreateCallForm()
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


@calls.route('/calls-list', methods=['GET'])
@login_required
def calls_list():
    calls = []
    calls_query = db.session.query(Call).filter(Call.user == current_user.id)
    for c in calls_query:
        phone_numbers = c.initial_phone_number + ', ' + ', '.join(c._phone_numbers.split(';'))
        # TODO: add s3 link
        calls.append((c.call_name, phone_numbers, 'TODO'))

    return render_template('calls/list_calls.html', calls=calls)


@calls.route('/test', methods=['GET'])
def test():
    e = PDFEngine(text="""[00:03:00] Speaker 2: This is Abby.
[00:09:00] Speaker 3: Hey Abby, this is Anis.
[00:09:00] Speaker 1: Hello. Is anyone there?
[00:14:00] Speaker 2:  Yeah, we're here Kerry. How are you doing?
[00:17:00] Speaker 1:  Oh great to hear you guys. How are you?
[00:20:00] Speaker 2:  I'm doing well. You're nice.
[00:21:00] Speaker 3:  All right, that's cut the chitchat get the business.
[00:23:00] Speaker 1:  How many money did you guys make last week?
[00:28:00] Speaker 2:  Okay, that's enough.
[00:28:00] Speaker 3:  It's not about the money. It's about the number Tau that we have.
[00:32:00] Speaker 1:  Oh, yes. I saw 70% growth from last one great work.
[00:31:00] Speaker 2:  All right, the car has to be less than a minute. So let them eat here.
[00:39:00] Speaker 3:  your oldest""", participants=["+12102683553", "+16502857265", "+12102683553"])
    return e.pdf_url, 200
