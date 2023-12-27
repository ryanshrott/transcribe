from openai import OpenAI
from keys import OPENAI_API_KEY, ANYSCALE_API_KEY, TOGETHER_API_KEY
from prompts import INITIAL_RESPONSE, system_prompt
import time

client = OpenAI(api_key=ANYSCALE_API_KEY,
                base_url = "https://api.endpoints.anyscale.com/v1")

system = '''You are currently assisting Ryan answer questions in a live technical interview for a software engineering role. A poor transcription of the conversation (in chronological order) will be given to you. Please respond to the most recent technical aspects of this conversation in order to assist Ryan answer technical aspects of the conversation. If there are multiple technical topics/queries in the trascript, ONLY respond to the latest topic at the end of the transcript. Confidently give a straightforward, short and concise response. DO NOT ask to repeat, and DO NOT ask for clarification. Don't clarify why you are discussing a certain topic. Do not make things up or role play. Do not greet the user. Only respond to topics in the transcript. If no technical content is found in the trascript, ONLY respond with 'no technical content' and do not explain why.'''

def generate_response_from_transcript(transcript):
    messages=[{'role': 'system', 'content': system},
              {'role': 'user', 'content': transcript}]
    print(messages)
    try:
        response = client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=messages,
                temperature = 0.0,
                stop=['no technical content', 'No technical content']
        )
    except Exception as e:
        print(e)
        return ''
    
    full_response = response.choices[0].message.content.strip()
    print(full_response)
    try:
        return full_response
    except:
        return ''
    
class GPTResponder:
    def __init__(self):
        self.response = INITIAL_RESPONSE
        self.response_interval = 2

    def respond_to_transcriber(self, transcriber):
        while True:
            if transcriber.transcript_changed_event.is_set():
                start_time = time.time()

                transcriber.transcript_changed_event.clear() 
                transcript_string = transcriber.get_transcript(reverse=True)

                response = generate_response_from_transcript(transcript_string)
                
                end_time = time.time()  # Measure end time
                execution_time = end_time - start_time  # Calculate the time it took to execute the function
                
                if response != '':
                    self.response = response

                remaining_time = self.response_interval - execution_time
                if remaining_time > 0:
                    time.sleep(remaining_time)
            else:
                time.sleep(0.3)

    def update_response_interval(self, interval):
        self.response_interval = interval