# Voice Cloner

This is a voice cloning project using ECAPA-TDNN for speaker embedding, F5-TTS for text-to-speech synthesis, and HiFi-GAN as the vocoder.

## Features
- Speaker embedding using ECAPA-TDNN
- Natural speech synthesis with F5-TTS
- High-quality vocoding with HiFi-GAN

## Usage
1. Clone this repo
2. Follow the steps in `run.py` to test voice cloning

arrange the folders according to the repo and run the commands
uvicorn api.main:app --reload
or 
python ui/interface.py
