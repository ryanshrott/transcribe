from openai import OpenAI
from keys import OPENAI_API_KEY
import whisper
import os
import torch

client = OpenAI(api_key=OPENAI_API_KEY)

def get_model(use_api):
    if use_api:
        return APIWhisperTranscriber()
    else:
        return WhisperTranscriber()

class WhisperTranscriber:
    def __init__(self):
        self.audio_model = whisper.load_model(os.path.join(os.getcwd(), 'tiny.en.pt'))
        print(f"[INFO] Whisper using GPU: " + str(torch.cuda.is_available()))

    def get_transcription(self, wav_file_path):
        try:
            result = self.audio_model.transcribe(wav_file_path, fp16=torch.cuda.is_available())
            print(result)
        except Exception as e:
            print(e)
            return 'error WhisperTranscriber'
        return result.strip()
    
class APIWhisperTranscriber:
    def get_transcription(self, wav_file_path):
        try:
            print('try')
            print(wav_file_path)
            with open(wav_file_path, "rb") as audio_file:
                result = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format='text')
                print(result)
        except Exception as e:
            print(e)
            return 'error APIWhisperTranscriber'
        return result.strip()