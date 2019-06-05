import nexmo
import base64
import uuid
import pdfkit
import boto3
import os
import s3transfer
import io
import matplotlib.pyplot as plt
from datetime import datetime
from jinja2 import Template
from collections import defaultdict

class PDFEngine:

    def __init__(self, participants=[], text=""):
        self.participants = participants
        self.number_of_participants = len(participants)
        self.from_number = os.getenv('NEXMO_NUMBER')
        api_key = os.getenv('NEXMO_API_KEY')
        print("apikey", api_key)
        self.nexmo_client = nexmo.Client(
            key=api_key, secret=os.getenv('NEXMO_SECRET'))
        self.pdf_url = self._processPDF(text)

    def _phone_format(self, n):
        return format(int(n[:-1]), ",").replace(",", "-") + n[-1]
        
    def _processPDF(self, call_transcript):

        transcript_object = self._parseTranscript(call_transcript)
        transcript_object, nlp_analysis = self._createNLPAnalysis(transcript_object)
        with open("./assets/meeting_note_template.html") as t:
            template = Template(t.read())
            current_date = datetime.today().strftime('%Y-%m-%d')
            pie_chart_url = self._createPieChartAndUpload(nlp_analysis)
            html = template.render(date = current_date, speakers = transcript_object, pie_chart = pie_chart_url)
        pdf_url = self._savePDF(html)
        return pdf_url


    def textPDF(self):
        body_text = "Here are the meeting notes for your recent conference call: " + self.pdf_url
        for num in self.participants:
            self._sendTextTo(self.from_number, num, body_text)
    
    def _createPDFURL(self):
        url = str(uuid.uuid4())
        return url + ".pdf"

    def _savePDF(self, html):
        url = self._createPDFURL()
        pdf_data = pdfkit.from_string(html, url)
        pdf_url = self._uploadFileToAWS(url[::-3] , url)
        self._deleteFile(url)
        return pdf_url
    
    def _deleteFile(self, path):
        os.remove(path)

    def _parseTranscript(self, text):
        lines = text.split('\n')
        transcript_objects = []
        for line in lines:
            timestamp = line[:10]
            split_lines = line.split(" ")
            speaker_number = split_lines[2]
            idx = int(speaker_number[:-1]) - 1
            corresponding_phone_number = self._phone_format(self.participants[idx])
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


    def _uploadImageToAWS(self, img_data, name, filetype=".png"):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('cs194w')
        bucket.put_object(Body=img_data, ContentType='image/png',
                          Key=str(name + filetype))
        return "https://s3-us-west-2.amazonaws.com/cs194w/" + str(name + filetype)


    def _createNLPAnalysis(self, transcript_object):
        word_tracker = defaultdict(list)
        s = ""
        for line in transcript_object:
            number = line[1]
            spoken_words = line[2]
            word_tracker[number] += [spoken_words.split(" ")]
            s += spoken_words
        total = 0
        for k, v in word_tracker.items():
            total += len(v)
        times = { k: len(v) / (total * 1.0) for k, v in word_tracker.items()}
        print(times)
        return transcript_object, times

    

    def _createPieChartAndUpload(self, d):
        plt.pie([float(v) for v in d.values()], labels=[str(k) for k in d.keys()],
                   autopct=None)
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        url = str(uuid.uuid4())
        img_url = self._uploadImageToAWS(img_data, url)
        return img_url
