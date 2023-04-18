import io
import os
import configparser

from google.cloud import speech
from google.oauth2 import service_account



# Create a ConfigParser object and read the INI file
config = configparser.ConfigParser()



# Get the path to the directory containing the script file
scriptDir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the config directory relative to the script file
configDir = os.path.join(scriptDir, "..", "config")

config.read(os.path.join(configDir, "keys.ini"))

# Get the API key values from the INI file
pushbulletKey = config['API Keys']['pushbullet']
openaiKey= config['API Keys']['openai']

# Imports the Google Cloud client library


# Path to your service account key file
key_path = os.path.join(configDir, "google2.json")



# Instantiates a client using your service account key file
credentials = service_account.Credentials.from_service_account_file(key_path)
client = speech.SpeechClient(credentials=credentials)

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    'recording_loud.wav')

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

# Configuration for the audio file
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
