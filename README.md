# 🎙️ Voice Cloner

**A modular, end-to-end voice cloning system that turns a short voice sample and any text into synthesized speech in the speaker's voice, exposed through a REST API (FastAPI) and an interactive web UI (Gradio).**

![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-Web%20UI-FF7C00)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?logo=pytorch&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)

---

## 📌 Overview

Voice Cloner is a speech-synthesis pipeline that takes two inputs, a **reference audio clip** of a speaker and a **text prompt**, and produces a new audio file of that text spoken in a voice resembling the reference speaker.

The project is organized as three independent stages (speaker encoding, speech synthesis, audio output), wrapped by a single inference function that is served through both a **FastAPI endpoint** and a **Gradio interface**. Keeping the stages decoupled means any component (for example the speaker encoder or the TTS model) can be swapped without touching the rest of the system.

## ✨ Features

- **Speaker embedding extraction** from a short audio sample using [Resemblyzer](https://github.com/resemble-ai/Resemblyzer) (a GE2E-trained speaker encoder)
- **Neural text-to-speech** using the pretrained multilingual, multi-speaker **YourTTS** model via [Coqui TTS](https://github.com/coqui-ai/TTS)
- **Waveform export** to 16-bit PCM `.wav` using SciPy
- **REST API** built with FastAPI (async file upload, auto-generated Swagger docs)
- **Web UI** built with Gradio (record from microphone, type text, play back the result)
- **Modular architecture**: encoder, TTS, and audio output are separate, replaceable modules
- **Docker support** for reproducible setup and deployment

## 🧠 How It Works

```
 ┌────────────────┐     ┌────────────────────┐     ┌─────────────────────┐     ┌──────────────┐
 │ Reference audio│ ──▶ │  Speaker Encoder   │ ──▶ │  TTS (YourTTS)      │ ──▶ │ Audio writer │ ──▶ cloned_output.wav
 │   (.wav / mic) │     │  (Resemblyzer)     │     │  text + embedding   │     │ (SciPy, int16)│
 └────────────────┘     └────────────────────┘     └─────────────────────┘     └──────────────┘
                                   ▲
                       Input text ─┘ (passed to the TTS stage)
```

1. **Encode:** the reference audio is preprocessed (resampling, normalization, silence trimming) and converted into a fixed-length **speaker embedding** that captures vocal identity.
2. **Synthesize:** the input text and the speaker embedding are passed to the pretrained **YourTTS** model, which generates the speech waveform (the model includes its own neural vocoder).
3. **Export:** the waveform is converted to 16-bit PCM and written to a `.wav` file.

`app/inference.py` orchestrates these steps in a single function, `clone_voice(audio_path, text)`, which both the API and the UI call.

## 🗂️ Project Structure

```
voice_clonning/
├── api/
│   └── main.py                  # FastAPI app: POST /clone endpoint
├── app/
│   ├── inference.py             # Pipeline orchestration: clone_voice()
│   ├── encoder/
│   │   └── extract_embedding.py # Speaker embedding (Resemblyzer VoiceEncoder)
│   ├── tts/
│   │   └── synthesize.py        # Text-to-speech (Coqui TTS / YourTTS)
│   └── vocoder/
│       └── vocode.py            # Waveform → 16-bit PCM .wav writer
├── ui/
│   └── interface.py             # Gradio web interface
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container build (see Docker section)
└── README.md
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9 |
| Speaker encoder | Resemblyzer (GE2E speaker verification model) |
| Text-to-speech | Coqui TTS, pretrained **YourTTS** (`tts_models/multilingual/multi-dataset/your_tts`) |
| Deep learning | PyTorch, TorchAudio |
| Audio / numerics | SciPy, NumPy |
| API | FastAPI, Uvicorn |
| UI | Gradio |
| Packaging | Docker |

## 🚀 Getting Started

### Prerequisites

- Python **3.9** (3.9 to 3.11 are supported by Coqui TTS)
- `pip` and (recommended) a virtual environment
- ~2 GB free disk space (the YourTTS model downloads on first run)
- Optional: Docker

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/voice_clonning.git
cd voice_clonning

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

> The pretrained YourTTS weights are downloaded automatically the first time the TTS module loads, so the first run takes longer.

### Run the Web UI (Gradio)

```bash
python ui/interface.py
```

Open the printed local URL (default `http://127.0.0.1:7860`), record or upload a voice sample, enter text, and play the cloned output.

### Run the REST API (FastAPI)

```bash
uvicorn api.main:app --reload
```

- Interactive docs: `http://127.0.0.1:8000/docs`

**Example request:**

```bash
curl -X POST "http://127.0.0.1:8000/clone?text=Hello%20from%20my%20cloned%20voice" \
     -F "file=@sample.wav"
```

**Response:**

```json
{ "output": "cloned_output.wav" }
```

| Method | Endpoint | Parameters | Description |
|---|---|---|---|
| `POST` | `/clone` | `file` (audio upload, multipart), `text` (query, default `"Hello there!"`) | Clones the uploaded voice and synthesizes `text`; returns the output file path |

## 🐳 Docker

Run the project in an isolated, reproducible environment. Example `Dockerfile`:

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential ffmpeg libsndfile1 espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000 7860

# Default: serve the REST API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t voice-cloner .

# Run the API
docker run -p 8000:8000 voice-cloner

# Run the Gradio UI instead
docker run -p 7860:7860 voice-cloner python ui/interface.py
```

> For the Gradio UI inside a container, set `server_name="0.0.0.0"` in `iface.launch()` so it is reachable from the host.

## 🔎 Design Decisions

- **Separation of concerns:** encoder, synthesizer, and audio writer live in their own modules, so each can be upgraded or replaced independently (e.g. swapping in a different speaker encoder or a newer TTS model).
- **Single inference entry point:** `clone_voice()` is the only function the interfaces call, so the API and UI always behave identically.
- **Pretrained models over training from scratch:** leverages state-of-the-art pretrained models to deliver zero-shot voice cloning without needing hours of data per speaker.
- **Two interfaces, one core:** a programmatic API for integration and a Gradio UI for quick demos.

## ⚠️ Limitations

- Output quality depends on the **length and cleanliness** of the reference audio (a few seconds of clear, noise-free speech works best).
- Inference is configured for **CPU** (`use_cuda=False`), so generation is slower than on a GPU.
- Output is written to fixed filenames (`input.wav`, `cloned_output.wav`), so concurrent requests would overwrite each other.
- The first request is slow because of model download and loading.

## 🗺️ Roadmap

- [ ] Unique temp filenames per request and a downloadable `FileResponse`
- [ ] GPU support (CUDA) via configuration flag
- [ ] Multi-language selection exposed in the API and UI
- [ ] Reference-audio validation (duration, format, sample rate)
- [ ] Unit tests and CI (GitHub Actions)
- [ ] `docker-compose` to run the API and UI together

## ⚖️ Responsible Use

Voice cloning technology can be misused for impersonation and fraud. Only clone voices you own or have **explicit permission** to use, and clearly disclose synthetic audio where appropriate. This project is intended for educational and research purposes.

## 🙏 Acknowledgements

- [Coqui TTS](https://github.com/coqui-ai/TTS) for the YourTTS model and TTS toolkit
- [Resemblyzer](https://github.com/resemble-ai/Resemblyzer) for the speaker encoder
- [FastAPI](https://fastapi.tiangolo.com/) and [Gradio](https://www.gradio.app/)

## 👤 Author

**Sagar**
Built during my 2nd year of engineering as a hands-on project in deep learning, speech synthesis, and API development.

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-profile](https://linkedin.com/in/your-profile)

---

⭐ If you found this project interesting, consider giving it a star!
