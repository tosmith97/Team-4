import os
from pydub.utils import mediainfo
from pydub import AudioSegment
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class SpeechToTextServiceClient:

    def __init__(self):
        #Environment variable
        self.client = speech.SpeechClient()

    def transcribeAudioFile(self, file_name=None):
        # Loads the audio into memory
        info = mediainfo(file_name)
        with open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=int(float(info['sample_rate'])),
            audio_channel_count=int(info['channels']),
            use_enhanced=True,
            model='phone_call',
            language_code='en-US')

        # Detects speech in the audio file
        response = self.client.recognize(config, audio)
        print(response)

        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

        return response.results

if __name__=="__main__":
    client = SpeechToTextServiceClient()
    filename = os.path.join(
                os.path.dirname(__file__),
                'recordings',
                'test3.wav')

    # a = AudioSegment.from_wav(filename)
    # a.export("./recordings/test4.flac", format="flac")
    client.transcribeAudioFile(filename)