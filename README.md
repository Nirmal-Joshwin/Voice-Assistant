# 🎙️ Voice Assistant

A Python-based desktop voice assistant with a dark-themed GUI, supporting both voice and text input. It handles system controls, file management, web lookups, and general Q&A through an LLM fallback — all from a single window.

---

## Features

- **Voice & Text Input** — Speak or type your commands
- **Speech Recognition** — Powered by `faster-whisper` (Whisper `small` model, runs locally on CPU)
- **Text-to-Speech** — Responds aloud using `pyttsx3`
- **System Controls** — Adjust volume (set/increase/decrease/mute) and screen brightness
- **App Launcher** — Open Chrome, Notepad, Calculator by voice
- **File System** — List files and get file size details
- **Web Search** — Wikipedia summaries for factual queries
- **LLM Fallback** — Routes to OpenRouter (auto model) when Wikipedia has no answer
- **Fuzzy Matching** — Understands natural phrasing variations via `rapidfuzz`
- **Dark UI** — Clean `tkinter` interface with a scrollable chat window

---

## Project Structure

```
Voice-Assistant/
├── main.py            # Entry point — launches the UI
├── ui.py              # Tkinter GUI (chat window, input, voice button)
├── assistant.py       # Command router with fuzzy intent matching
├── speech.py          # Audio recording, Whisper transcription, pyttsx3 TTS
├── system_control.py  # Volume & brightness control (Windows)
├── file_system.py     # List files, file details, open files
├── web_search.py      # Wikipedia summary lookup
├── llm.py             # OpenRouter API integration (LLM fallback)
├── utils.py           # Time/date helpers, query text cleaner
└── requirements.txt   # Python dependencies
```

---

## Requirements

- **Python** 3.8+
- **Windows** (system controls use Windows-specific APIs)
- **Microphone** for voice input

### Python Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
pip install faster-whisper
```

`requirements.txt` includes:
```
sounddevice
vosk
pyttsx3
requests
wikipedia
beautifulsoup4
rapidfuzz
```

> **Note:** `faster-whisper` is not listed in `requirements.txt` but is required by `speech.py`. Install it separately as shown above.

---

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nirmal-Joshwin/Voice-Assistant.git
   cd Voice-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install faster-whisper
   ```

3. **Configure your OpenRouter API key**

   Open `llm.py` and replace the placeholder key:
   ```python
   API_KEY = "your-openrouter-api-key-here"
   ```
   Get a free key at [openrouter.ai](https://openrouter.ai).

4. **Run the assistant**
   ```bash
   python main.py
   ```

---

## Usage

Once launched, a dark-themed chat window appears.

| Method | How to use |
|--------|-----------|
| **Text** | Type a command in the input box and click **Send** |
| **Voice** | Click **🎤 Speak** and talk — the assistant listens for ~3 seconds |

### Example Commands

| Command | What it does |
|---------|-------------|
| `What time is it?` | Returns the current time |
| `What's today's date?` | Returns the current date |
| `Set volume to 60` | Sets system volume to 60% |
| `Increase volume` | Raises the volume |
| `Mute` | Mutes audio |
| `Set brightness to 80` | Sets screen brightness to 80 |
| `Open Chrome` | Launches Google Chrome |
| `Open Notepad` | Launches Notepad |
| `List files` | Shows files in the current directory |
| `Who is Elon Musk?` | Fetches a Wikipedia summary |
| `What is quantum computing?` | Wikipedia → LLM fallback if not found |
| `Exit` / `Quit` | Closes the assistant |

---

## How It Works

```
User Input (voice or text)
        ↓
  assistant.py  ←── fuzzy intent matching (rapidfuzz)
        ↓
  ┌─────────────────────────────────────┐
  │  System control / File / Time/Date  │  ← direct response
  │  Web query → Wikipedia summary      │  ← web_search.py
  │  No Wikipedia result → LLM          │  ← llm.py (OpenRouter)
  └─────────────────────────────────────┘
        ↓
  speech.py → pyttsx3 (speaks response)
        ↓
  ui.py → displays response in chat
```

---

## Platform Notes

This assistant is built for **Windows only**. The following features use Windows-specific APIs:

- Volume control — `powershell` SendKeys + `ctypes.windll.winmm`
- Brightness control — `WmiMonitorBrightnessMethods` via PowerShell
- File opening — `os.startfile()`

Linux/macOS support would require replacing `system_control.py` with platform-appropriate commands.

---

## License

MIT License — free to use, modify, and distribute.
