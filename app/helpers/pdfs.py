import nexmo
from app import create_app
import base64
import uuid
import pdfkit

class PDFEngine:

    # TODO: Put object creation on the task queue
    def __init__(self, number_of_participants=2, text=""):
        self.app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        self.number_of_participants = number_of_participants
        with app.app_context():
            self.from_number = app.config['NEXMO_NUMBER']
            self.nexmo_client = nexmo.Client(
                key=app.config['NEXMO_API_KEY'], secret=app.config['NEXMO_SECRET'])
        # TODO: Save pdf_url to database for frontend
        self.pdf_url = self._processPDF(text)
        
    # TODO: As we scale, want multiple numbers. For now, .env works
    def _getNexmoNumber(self):
        pass

    # TODO:
    def _processPDF(self, call_transcript):
        html = self._parseTranscript(call_transcript)
        pdf_url = self._savePDF(html)
        return pdf_url


    def textPDF(self, numbers_list):
        body_text = "Here are the meeting notes for your recent conference call: " + self.pdf_url
        for num in numbers_list:
            _sendTextTo(self.from_number, num, body_text)
    
    def _createPDFURL(self, file_path):
        url = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        return file_path + url + ".pdf"

    # TODO: Remove inline
    def _savePDF(self, html):
        pdf_url = self._createPDFURL("./static/call_pdfs")
        pdfkit.from_string('Hello!', pdf_url)
        return pdf_url
    
    # TODO: Need Google Transcript to start parsing
    def _parseTranscript(self, text):
        pass

    def _sendTextTo(self, from_number, to_number, text):
        self.nexmo_client.send_message(
            {'from': from_number, 'to': to_number, 'text': text})

