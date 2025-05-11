import numpy as np
from scipy.io.wavfile import write

def save_audio(wav_tensor, path="output.wav", sample_rate=22050):
    audio = (wav_tensor * 32767).astype("int16")
    write(path, sample_rate, audio)
