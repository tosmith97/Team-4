import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class SpeechToTextServiceClient:

    def __init__(self):
        #Environment variable
        self.client = speech.SpeechClient()

    def transcribeAudioFile(self, file_name=None):
        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            model='phone_call',
            language_code='en-US')

        # Detects speech in the audio file
        response = self.client.recognize(config, audio)
        print(response)

        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

        # return response.results[0]

if __name__=="__main__":
    client = SpeechToTextServiceClient()
    filename = os.path.join(
                os.path.dirname(__file__),
                'recordings',
                'test2.flac')
    client.transcribeAudioFile(filename)
