from pydub import AudioSegment
from pydub.utils import mediainfo
import SpeechToTextServiceClient as STTS

from io import BytesIO
import os
import datetime
import nexmo
import wave

URL = "https://api.nexmo.com/v1/files/a0a01d31-69b5-47f4-a9c2-f8c3c5fbe7df"

client = nexmo.Client(
    application_id='4811d796-b14a-4775-b13c-4a93dec02e98',
    private_key='private.key',
)

response = client.get_recording(URL)
fn = os.path.join(*[os.getcwd(), 'recordings', datetime.date.today().strftime('%Y-%m-%d') + '.wav'])
# with open(fn, "wb+") as f:
#     f.write(response)
# a = AudioSegment.from_file(fn)

# with wave.open(fn, "wb") as wf:
#     wf.setnchannels(2)
#     wf.setsampwidth(2)
#     wf.setframerate(16000)
#     wf.writeframes(response)

a = AudioSegment.from_file(BytesIO(response), channels=2, sample_width=2, frame_rate=16000)
a.export(fn, format="wav")
info = mediainfo(fn)
print(info)
STTClient = STTS.SpeechToTextServiceClient()
print(STTClient.transcribeAudioFile(fn))
