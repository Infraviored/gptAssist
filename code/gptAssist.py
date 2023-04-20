import speech_recognition as sr
from pydub import AudioSegment
import io
from io import BytesIO
import os
import configparser
import asyncio
import librosa.effects as effects
import librosa

from pydub import AudioSegment, playback, effects



from google.oauth2 import service_account
from google.cloud import speech
from google.cloud import texttospeech

import openai
import pushbullet

from EdgeGPT import Chatbot, ConversationStyle
import json
import re

config = configparser.ConfigParser()



codeDir = os.path.dirname(os.path.abspath(__file__))
configDir = os.path.join(codeDir, "..", "config")
audioDir = os.path.join(codeDir, "..", "audio")
config.read(os.path.join(configDir, "keys.ini"))

# Get the API key values from the INI file
pushbulletKey = config['API Keys']['pushbullet']
openaiKey= config['API Keys']['openai']
googleKey = os.path.join(configDir, "google_stt_for_gpt.json")

with open(os.path.join(configDir, "bingCookie.json"), 'r') as f:
    bingCookie = json.load(f)

# Instantiates a client using your service account key file
credentials = service_account.Credentials.from_service_account_file(googleKey)
transcriber = speech.SpeechClient(credentials=credentials)
speaker = texttospeech.TextToSpeechClient(credentials=credentials)






wavConfig = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='de-DE')





# Create a recognizer object
recognizer = sr.Recognizer()


emojis = {'😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '🥹', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😮‍💨', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🫣', '🤗', '🫡', '🤔', '🫢', '🤭', '🤫', '🤥', '😶', '😶‍🌫️', '😐', '😑', '😬', '🫨', '🫠', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '😵‍💫', '🫥', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾'}

def assistifyString(input_string):
    # Remove everything that looks like [^3^], [^4^], etc.
    output_string = re.sub(r'\[\^\d+\^\]', '', input_string)
    
    # Remove "Hallo, das ist Bing. "
    output_string = output_string.replace('Hallo, das ist Bing. ', '')
    output_string = output_string.replace('```markdown', '')
    for emoji in emojis:
        output_string = output_string.replace(emoji, '')
    
    return output_string


def speech_to_text_cloud(recording):
    # Loads the audio into memory
    with io.open(recording, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
    # Detects speech in the audio file
    response = transcriber.recognize(config=wavConfig, audio=audio)
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript
    


def text_to_speech(text, output_file, voiceModel = "D"):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="de-DE", 
        name = 'de-DE-Wavenet-%s' % voiceModel,
#        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = speaker.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content contains the binary representation of the audio waveform for the requested synthesis
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')


def play_audio(file_name, pitch=0):
    y, sr = librosa.load(file_name, sr=None)
    if pitch != 0:
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch)
        sound = AudioSegment(y_shifted.tobytes(), frame_rate=sr, sample_width=y_shifted.dtype.itemsize, channels=len(y_shifted.shape))
    else:
        sound = AudioSegment.from_file(file_name, format="mp3")
    playback.play(sound)



BingWakewordList = ("bing", "being" , "bink", 'halloween', 'ping')
BingWakeword = "bing"
JarvisWakeword = "jarvis"

def get_wake_word(phrase):
    for i in BingWakewordList:
        if i in phrase.lower():
            return BingWakeword
    if JarvisWakeword in phrase.lower():
        return JarvisWakeword
    else:
        return None
    


# Use the default microphone as the audio source
def recordAudio(filename):
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
        #audio_data_loud = audio_data + 30

        # Save the modified audio to a WAV file
        with open(os.path.join(audioDir, filename), "wb") as f:
            f.write(audio_data.export(format="wav").read())

        # # Save the modified audio to an MP3 file
        # with open(os.path.join(audioDir, "%s.mp3" %filename), "wb") as f:
        #     f.write(audio_data_loud.export(format="mp3").read())

        print("Recording saved!")

def transcribeFile(file_name, config):
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        response = transcriber.recognize(config=config, audio=audio)
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
                        print(transcription)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            print('Wake word %s detected.' % wake_word)
            
            if wake_word == BingWakeword:
                play_audio("BingC.wav")
            if wake_word == JarvisWakeword:
                play_audio("JarvisE.wav")

            if wake_word == BingWakeword:
                transcript = ""
                while not transcript == "stop":
                    audio = recognizer.listen(source)
                    print("Speak a prompt...")
                    try:
                        with open("audio_prompt.wav", "wb") as f:
                            f.write(audio.get_wav_data())
                    except Exception as e:
                        print(e)

                    transcript = speech_to_text_cloud("audio_prompt.wav")
                    if transcript == "stop" or transcript == None:
                        pass
                    else:
                        bot = Chatbot(cookies=bingCookie)
                        response = await bot.ask(prompt=transcript, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
                        for message in response["item"]["messages"]:
                            if message["author"] == "bot":
                                bot_response = message["text"]
                                print(bot_response)
                                text_to_speech(assistifyString(bot_response), "bing_response.wav", "C")
                                play_audio("bing_response.wav")
                                break
                            

            # if wake_word == JarvisWakeword:
            #     play_audio("JarvisE.wav")
            #                     # Send prompt to GPT-3.5-turbo API
            #     response = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo",
            #         messages=[
            #             {"role": "system", "content":
            #             "You are a helpful assistant."},
            #             {"role": "user", "content": user_input},
            #         ],
            #         temperature=0.5,
            #         max_tokens=150,
            #         top_p=1,
            #         frequency_penalty=0,
            #         presence_penalty=0,
            #         n=1,
            #         stop=["\nUser:"],
            #     )

            #     bot_response = response["choices"][0]["message"]["content"]
            #     print("Bot's response:", bot_response)


if __name__ == "__main__":
    asyncio.run(main())


# recordAudio("ok_bing.wav")
# recording_loud = os.path.join(audioDir, 'ok_bing.wav')
# transcribeFile(recording_loud, wavConfig)

# play_audio("JarvisE.wav")



# play_audio("BingC.wav")

