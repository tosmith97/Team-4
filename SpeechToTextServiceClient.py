import os
from pydub.utils import mediainfo
from pydub import AudioSegment
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class SpeechToTextServiceClient:

    def __init__(self):
        #Environment variable GOOGLE_APPLICATION_CREDENTIALS needs to
        # be set to googleauth-adde97af7066
        self.client = speech.SpeechClient()

    def transcribeAudioFile(self, file_name, file_format='wav'):
        # Loads the audio into memory
        info = mediainfo(file_name)
        with open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        if file_format == 'flac':
            encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        elif file_format == 'wav':
            encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        else:
            print("Error: only .flac and .wav formats are supported.")
            return

        config = types.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=int(float(info['sample_rate'])),
            audio_channel_count=int(info['channels']),
            use_enhanced=True,
            model='phone_call',
            language_code='en-US')

        # Detects speech in the audio file
        response = self.client.recognize(config, audio)

        transcript = 'Transcript: '
        for result in response.results:
            transcript += result.alternatives[0].transcript
        print(transcript)
        return transcript

if __name__=="__main__":
    client = SpeechToTextServiceClient()
    filename = os.path.join(
                os.path.dirname(__file__),
                'recordings',
                'test.wav')

    client.transcribeAudioFile(filename)
