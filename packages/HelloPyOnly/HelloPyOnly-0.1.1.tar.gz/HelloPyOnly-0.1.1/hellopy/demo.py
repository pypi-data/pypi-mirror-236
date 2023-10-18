import pyaudio

from hellopy.window import window
from hellopy.mouse import mouse

__all__ = ['stream']

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)