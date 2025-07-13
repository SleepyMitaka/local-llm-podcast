# LLM Podcast Project (Looping + Custom Voices)

This version runs a looping podcast with 3 LLM agents, each using their own **custom-trained XTTS voice** from `.wav` files.

## Setup

1. Install [Ollama](https://ollama.com) and pull a model (e.g. `ollama pull llama3`).
2. Install Python packages:
```bash
pip install -r requirements.txt
```
3. Install `ffmpeg`.
4. Add your `.wav` samples to the `voices/` folder:
   - `voices/tony.wav`
   - `voices/zay.wav`
   - `voices/max.wav`
5. Run the app:
```bash
python main.py
```

## Notes
- It loops endlessly until stopped (Ctrl+C).
- XTTS will clone the speaker identity from your provided `.wav` files.

## Credits
- i got this idea from dougdougs stream where he did a simillar llm podcast using chatgpt
- i got the idea to use xtts from kimjammers neuro project check him out!
