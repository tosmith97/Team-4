import nexmo
# from app import create_app
import base64
import uuid
import pdfkit
import boto3
import os
import s3transfer

class PDFEngine:

    # TODO: Put object creation on the task queue
    def __init__(self, number_of_participants=2, text=""):
        # self.app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        self.number_of_participants = number_of_participants
        # with app.app_context():
        self.from_number = os.getenv('NEXMO_NUMBER')
        self.nexmo_client = nexmo.Client(
            key=os.getenv('NEXMO_API_KEY'), secret=os.getenv('NEXMO_SECRET'))
        # TODO: Save pdf_url to database for frontend
        self.pdf_url = self._processPDF(text)
        
    # TODO: As we scale, want multiple numbers. For now, .env works
    def _getNexmoNumber(self):
        pass

    # TODO:
    def _processPDF(self, call_transcript):
        html = """<!doctype html >

                THIS IS A TEST
                <html lang = "en" >
                </html>
                """
        # html = self._parseTranscript(call_transcript)
        pdf_url = self._savePDF(html)
        return pdf_url


    def textPDF(self, numbers_list):
        body_text = "Here are the meeting notes for your recent conference call: " + self.pdf_url
        for num in numbers_list:
            self._sendTextTo(self.from_number, num, body_text)
    
    def _createPDFURL(self):
        url = str(uuid.uuid4())
        return url + ".pdf"

    # TODO: Remove inline
    def _savePDF(self, html):
        # TODO make no file needed
        url = self._createPDFURL()
        pdf_data = pdfkit.from_string(html, url)
        pdf_url = self._uploadFileToAWS(url[::-3] , url)
        self._deleteFile(url)
        return pdf_url
    
    def _deleteFile(self, path):
        os.remove(path)


    # TODO: Need Google Transcript to start parsing
    def _parseTranscript(self, text):
        pass

    def _sendTextTo(self, from_number, to_number, text):
        self.nexmo_client.send_message(
            {'from': from_number, 'to': to_number, 'text': text})


    # TODO: name is a timestamp of date + UUID 4 digits

    def _uploadFileToAWS(self, name, data):
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        s3 = boto3.resource('s3')
        print(name)
        # bucket_location = boto3.client(
        #     's3').get_bucket_location(Bucket='cs194w')
        s3.meta.client.upload_file(data, 'cs194w', name + ".pdf", ExtraArgs={
                                   'ACL': 'public-read'})
        # object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        #     bucket_location['LocationConstraint'],
        #     'cs194w',
        #     name)

        return "https: // s3-us-west-2.amazonaws.com/cs194w/" + name + ".pdf"
