import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Create a recognizer object
r = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    # Adjust for ambient noise
    r.adjust_for_ambient_noise(source)

    # Prompt the user to speak
    print("Start speaking now...")

    # Record the audio for 5 seconds
    audio = r.listen(source, phrase_time_limit=5)

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