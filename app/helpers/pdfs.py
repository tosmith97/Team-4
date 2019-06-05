import nexmo
import base64
import uuid
import pdfkit
import boto3
import os
import s3transfer
from datetime import datetime
from jinja2 import Template

class PDFEngine:

    # TODO: Put object creation on the task queue
    def __init__(self, participants=[], text=""):
        self.participants = participants
        self.number_of_participants = len(participants)
        self.from_number = os.getenv('NEXMO_NUMBER')
        api_key = os.getenv('NEXMO_API_KEY')

        self.nexmo_client = nexmo.Client(
            key=api_key, secret=os.getenv('NEXMO_SECRET'))
        # TODO: Save pdf_url to database for frontend
        self.pdf_url = self._processPDF(text)
        
    # TODO: As we scale, want multiple numbers. For now, .env works
    def _getNexmoNumber(self):
        pass

    # TODO:
    def _processPDF(self, call_transcript):
        transcript_object = self._parseTranscript(call_transcript)
        cwd = os.getcwd()
        rel_path = "app/assets/meeting_note_template.html"
        note_template = os.path.join(cwd, rel_path)
        with open(note_template) as t:
            template = Template(t.read())
            current_date = datetime.today().strftime('%Y-%m-%d')
            html = template.render(date = current_date, speakers = transcript_object)
        pdf_url = self._savePDF(html)
        return pdf_url


    def textPDF(self):
        body_text = "Here are the meeting notes for your recent conference call: " + self.pdf_url
        for num in self.participants:
            self._sendTextTo(self.from_number, num, body_text)
    
    def _createPDFURL(self):
        url = str(uuid.uuid4())
        return url + ".pdf"

    # TODO: Remove inline
    def _savePDF(self, html):
        url = self._createPDFURL()
        pdf_data = pdfkit.from_string(html, url)
        pdf_url = self._uploadFileToAWS(url[::-3] , url)
        self._deleteFile(url)
        return pdf_url
    
    def _deleteFile(self, path):
        os.remove(path)

    # TODO: Need Google Transcript to start parsing
    def _parseTranscript(self, text):
        lines = text.split('\n')
        transcript_objects = []
        for line in lines:
            timestamp = line[:10]
            split_lines = line.split(" ")
            speaker_number = split_lines[2]
            idx = int(speaker_number[:-1]) - 1
            corresponding_phone_number = self.participants[idx]
            quotation = " ".join(split_lines[3:])
            transcript_objects.append(
                (timestamp, corresponding_phone_number, quotation))
        return transcript_objects

    def _sendTextTo(self, from_number, to_number, text):
        response = self.nexmo_client.send_message(
            {'from': from_number, 'to': to_number, 'text': text})
        response = response['messages'][0]
        if response['status'] == '0':
            print('Sent message', response['message-id'])
            print('Remaining balance is', response['remaining-balance'])
        else:
            print('Error:', response['error-text'])

    def _uploadFileToAWS(self, name, data):
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(data, 'cs194w', name + ".pdf", ExtraArgs={
                                   'ACL': 'public-read'})
        return "https://s3-us-west-2.amazonaws.com/cs194w/" + name + ".pdf"
