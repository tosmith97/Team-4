import json
from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
    jsonify,
    current_app
)

from flask_rq import get_queue

from app import db

from app.models import User
from string import Template
from flask import current_app
import uuid
import urllib

calls = Blueprint('calls', __name__)


@calls.route('/ncco', methods=['GET', 'POST'])
def start_call():
    request_data = json.loads(request.data)
    ncco_data = {}
    ncco_data['hostname'] = current_app.config['HOST_NAME']
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
    print(request.data)
    return "", 200


@calls.route('/recordings', methods=['GET', 'POST'])
def call_recordings():
    print(request.data)
    print("RECORDING")
    return "", 200
