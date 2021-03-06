import speech_recognition as sr
from os import path


def printWAV(FILE_NAME, pos, clip):
    # use the audio file as the audio source
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)),
                           'static/' + FILE_NAME)
    r = sr.Recognizer()
    text = "start here: "
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source, duration=clip, offset=pos)
        # recognize speech using Google Speech Recognition
        try:
            text += r.recognize_google(audio) + "\n"
        except sr.UnknownValueError:
            text += f'Could not understand audio!{clip} , {pos},\n'
        except sr.RequestError as e:
            text += "Could not request results; {0}".format(e) + "\n"
    return text

# def main():
#     FILE_NAME = "english.wav"
#     time = 0 # position in track
#     dur = 10 # clip length to process each iteration
#     text = printWAV(FILE_NAME, time, dur) # pos = 0 and clip = 10
#     print(text)
# main()
