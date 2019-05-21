from pydub import AudioSegment
from pydub.utils import mediainfo
import SpeechToTextServiceClient as STTS

from io import BytesIO
import os
import datetime
import nexmo
import wave

URL = "https://api.nexmo.com/v1/files/0ed9fd40-b905-4c25-8bb1-37c4b1cbcd64"

def from_URL(url):
    client = nexmo.Client(
        application_id='4811d796-b14a-4775-b13c-4a93dec02e98',
        private_key='private.key',
    )
    response = client.get_recording(url)
    fn = os.path.join(*[os.getcwd(), 'recordings', datetime.date.today().strftime('%Y-%m-%d') + '.wav'])

    a = AudioSegment.from_file(BytesIO(response), channels=3, sample_width=2, frame_rate=16000)
    a.export(fn, format="wav")
    return fn

# fn = os.path.join(os.getcwd(),
#                  'recordings',
#                  '4f33cd4e-2bcf-4e01-bf68-9aac36177de7.wav')
fn = from_URL(URL)
print(mediainfo(fn))
STTClient = STTS.SpeechToTextServiceClient()
transcript = STTClient.transcribeAudioFile(fn, True)
STTClient.saveTranscriptAsTxt(transcript, '1')
