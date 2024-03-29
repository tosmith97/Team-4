import os
from datetime import datetime
from pydub.utils import mediainfo
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech

import soundfile

class SpeechToTextServiceClient:

    def __init__(self):
        #Environment variable GOOGLE_APPLICATION_CREDENTIALS needs to
        # be set to googleauth-adde97af7066
        self.client = speech.SpeechClient()

    def transcribeAudioFile(self, file_name, multichannel=False, file_format='wav'):
        # comment out if your computer treats original file as 16 bit
        # s/o to my computer for not doing that
        # data, samplerate = soundfile.read(file_name)
        # soundfile.write(file_name, data, samplerate, subtype='PCM_16')

        # Loads the audio into memory
        info = mediainfo(file_name)
        with open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.types.RecognitionAudio(content=content)
        # print(info)
        if file_format == 'flac':
            encoding = speech.enums.RecognitionConfig.AudioEncoding.FLAC
        elif file_format == 'wav':
            encoding = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16
        else:
            print("Error: only .flac and .wav formats are supported.")
            return

        if multichannel:
            config = speech.types.RecognitionConfig(
                encoding=encoding,
                sample_rate_hertz=int(float(info['sample_rate'])),
                audio_channel_count=int(info['channels']),
                use_enhanced=True,
                enable_separate_recognition_per_channel=True,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True,
                model='phone_call',
                language_code='en-US')
        else:
            config = speech.types.RecognitionConfig(
                encoding=encoding,
                sample_rate_hertz=int(float(info['sample_rate'])),
                use_enhanced=True,
                enable_speaker_diarization=True,
                diarization_speaker_count=4,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True,
                model='phone_call',
                language_code='en-US')

        # Detects speech in the audio file
        response = self.client.recognize(config, audio)
        if multichannel:
            return self.transcribeMultichannel(response.results)
        else:
            return self.diarizeTranscript(response.results[-1].alternatives[0].words)

    def transcribeMultichannel(self, results):
        transcript = ""
        for i, res in enumerate(results):
            ts = res.alternatives[0].words[0].start_time
            transcript += "[%02d:%02d:%02d] " % (ts.seconds // 60,
                                                 ts.seconds % 60,
                                                 int(ts.nanos * 1e-9))
            transcript += "Speaker %d: " % res.channel_tag
            transcript += res.alternatives[0].transcript
            if i != len(results) - 1: 
                transcript += "\n"
        return transcript

    def diarizeTranscript(self, words):
        started = False
        transcript = ""
        for w in words:
            if not started:
                transcript += "[%02d:%02d:%02d] " % (w.start_time.seconds // 60,
                                                     w.start_time.seconds % 60,
                                                     int(w.start_time.nanos * 1e-9))
                transcript += "Speaker %d: " % w.speaker_tag
                started = True
            transcript += w.word + " "
            if w.word.rstrip()[-1] == ".":
                transcript += "\n"
                started = False

        return transcript

    def saveTranscriptAsTxt(self, transcript, uuid):
        print(transcript)
        transcript_fn = os.path.join(*[os.getcwd(), 'transcripts', uuid + '.txt'])
        with open(transcript_fn, 'w+') as f:
            f.write(transcript)
        print('finished')


if __name__=="__main__":
    client = SpeechToTextServiceClient()
    filename = os.path.join(
                os.path.dirname(__file__),
                'recordings',
                '2019-05-13.wav')

    # a = AudioSegment.from_file(filename)
    # a.export('test4.wav', format='wav')

    transcript = client.transcribeAudioFile(filename)
    client.saveTranscriptAsTxt(transcript, '1')
