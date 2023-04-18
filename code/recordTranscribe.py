import speech_recognition as sr
from pydub import AudioSegment
import io
from io import BytesIO
import os
import configparser
import asyncio


from google.oauth2 import service_account
from google.cloud import speech



config = configparser.ConfigParser()


codeDir = os.path.dirname(os.path.abspath(__file__))
configDir = os.path.join(codeDir, "..", "config")
audioDir = os.path.join(codeDir, "..", "audio")
config.read(os.path.join(configDir, "keys.ini"))

# Get the API key values from the INI file
pushbulletKey = config['API Keys']['pushbullet']
openaiKey= config['API Keys']['openai']
googleKey = os.path.join(configDir, "google2.json")

# Instantiates a client using your service account key file
credentials = service_account.Credentials.from_service_account_file(googleKey)
client = speech.SpeechClient(credentials=credentials)




# The name of the audio file to transcribe
recording_loud = os.path.join(audioDir, 'recording_loud.wav')

wavConfig = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='en-US')



# Create a recognizer object
recognizer = sr.Recognizer()

BING_WAKE_WORD = "bing"
GPT_WAKE_WORD = "jarvis"

def get_wake_word(phrase):
    if BING_WAKE_WORD in phrase.lower():
        return BING_WAKE_WORD
    elif GPT_WAKE_WORD in phrase.lower():
        return GPT_WAKE_WORD
    else:
        return None
    


# Use the default microphone as the audio source
def recordAudio():
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Prompt the user to speak
        print("Start speaking now...")

        # Record the audio for 5 seconds
        audio = recognizer.listen(source, phrase_time_limit=5)

        # Load the audio data using pydub
        audio_bytes = audio.get_wav_data()
        audio_data = AudioSegment.from_wav(BytesIO(audio_bytes))

        # Increase the volume by 30 decibels
        audio_data_loud = audio_data + 30

        # Save the modified audio to a WAV file
        with open("recording_loud.wav", "wb") as f:
            f.write(audio_data_loud.export(format="wav").read())

        # Save the modified audio to an MP3 file
        with open("audio_loud.mp3", "wb") as f:
            f.write(audio_data_loud.export(format="mp3").read())

        print("Recording saved!")

def transcribeFile(file_name, config):
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))




async def main():
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(f"Waiting for wake words 'ok bing' or 'ok chat'...")
            while True:
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    wake_word = get_wake_word(transcription)

                    if wake_word is not None:
                        break
                    else:
                        print("Not a wake word. Try again.")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            print('Wake word %s detected. Starting transcription...' % wake_word)


# if __name__ == "__main__":
#     asyncio.run(main())

transcribeFile(recording_loud, wavConfig)