from app.encoder.extract_embedding import get_speaker_embedding
from app.tts.synthesize import synthesize_spectrogram
from app.vocoder.vocode import save_audio

def clone_voice(audio_path, text):
    embedding = get_speaker_embedding(audio_path)
    generated_wav = synthesize_spectrogram(text, speaker_embedding=embedding)
    save_audio(generated_wav, "cloned_output.wav")
    return "cloned_output.wav"
