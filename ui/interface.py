import gradio as gr
from app.inference import clone_voice

def run_clone(audio, text):
    audio_path = audio.name
    output = clone_voice(audio_path, text)
    return output

iface = gr.Interface(
    fn=run_clone,
    inputs=[
        gr.Audio(source="microphone", type="filepath", label="🎙️ Record your voice"),
        gr.Textbox(label="📝 Text to Speak", placeholder="Type the text here...")
    ],
    outputs=gr.Audio(type="filepath", label="🔊 Cloned Voice Output"),
    title="Voice Cloner",
    description="Record your voice and clone it with any input text."
)

iface.launch()
