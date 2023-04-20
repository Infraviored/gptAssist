import pydub
from pydub import playback

# plays an mp3 file
def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

play_audio('output.mp3')
