from TTS.api import TTS

# Load YourTTS pretrained model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False)

def synthesize_spectrogram(text: str, speaker_embedding):
    # Generate waveform directly (YourTTS includes vocoder)
    wav = tts.tts(text=text, speaker_embedding=speaker_embedding, use_cuda=False)
    return wav
