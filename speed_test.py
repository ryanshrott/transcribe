from openai import OpenAI
from keys import ANYSCALE_API_KEY, TOGETHER_API_KEY
import time
import json

# Initialize the API clients for AnyScale and Together
client_anyscale = OpenAI(api_key=ANYSCALE_API_KEY, base_url="https://api.endpoints.anyscale.com/v1")
client_together = OpenAI(api_key=TOGETHER_API_KEY, base_url='https://api.together.xyz')

system = '''You are currently assisting Ryan answer questions in a live technical interview for a software engineering role. A poor transcription of the conversation (in chronological order) will be given to you. Please respond to the most recent technical aspects of this conversation in order to assist Ryan answer technical aspects of the conversation. If there are multiple technical topics/queries in the trascript, ONLY respond to the latest topic at the end of the transcript. Confidently give a straightforward, short and concise response. DO NOT ask to repeat, and DO NOT ask for clarification. Don't clarify why you are discussing a certain topics. Do not make things up or role play. Do not greet the user. Only respond to topics in the transcript. If no technical content is found in the trascript, ONLY respond with 'no technical content' and do not explain why.'''

transcript = '''Ryan: [It's really nice to see you again, Ryan. Let's get started, if that's alright with you.]\n\nRyan: [That's nice. We went actually just went to the musicals 42nd Street.]\n\nRyan: [Can you discuss numerical partial differential equations in finance?]\n\nRyan: [and discuss polymorphism in C-sharp.]\n\nBob: [you]\n\nRyan: [with a simple example of polymorphism.]\n\nRyan: [Discuss the latest trends in large language models.]\n\nRyan: [Can you discuss the flash attention scheme in large language models?]\n\nRyan: [Why are GPUs important in large language models?]\n\nRyan: [Can you discuss the advantages of open-source models over closed-source?]'''

def generate_response_from_transcript(client, transcript):
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': transcript}]
    start_time = time.time()
    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=messages,
        temperature=0.0,
        stop=['no technical content', 'No technical content']
    )
    response = response.choices[0].message.content.strip()
    end_time = time.time()
    return response, end_time - start_time

def test_api(client, name, trials=10):
    responses = []
    total_time = 0

    for _ in range(trials):
        response, duration = generate_response_from_transcript(client, transcript)
        responses.append(response)
        total_time += duration

    # Save the responses and timing information
    with open(f"{name}_responses.json", "w") as file:
        json.dump({
            "average_time": total_time / trials,
            "responses": [r for r in responses]  # Extracting response data
        }, file, indent=4)

    print(f"Completed {trials} trials for {name} with an average response time of {total_time / trials} seconds.")

# Test Together API
test_api(client_together, "together")

# Test AnyScale API
test_api(client_anyscale, "anyscale")

