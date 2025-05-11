from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

encoder = VoiceEncoder()

def get_speaker_embedding(audio_path: str) -> np.ndarray:
    wav = preprocess_wav(audio_path)
    embed = encoder.embed_utterance(wav)
    return embed
