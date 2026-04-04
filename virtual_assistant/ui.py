import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

from speech import SpeechEngine
from assistant import Assistant


class AssistantUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Assistant")
        self.root.geometry("650x550")

        self.speech = SpeechEngine()
        self.assistant = Assistant()

        self.build_ui()

    def build_ui(self):
        self.root.configure(bg="#1e1e1e")

        # Chat display
        self.chat = scrolledtext.ScrolledText(
            self.root,
            bg="#121212",
            fg="white",
            font=("Consolas", 11),
            wrap=tk.WORD
        )
        self.chat.pack(fill="both", expand=True, padx=10, pady=10)

        # Input frame
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(fill="x", padx=10, pady=5)

        self.input = tk.Entry(
            frame,
            font=("Consolas", 12)
        )
        self.input.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ttk.Button(frame, text="Send", command=self.text_input).pack(side="left")
        ttk.Button(frame, text="🎤 Speak", command=self.voice_input).pack(side="left")
        
    def append(self, text):
        self.chat.insert(tk.END, text + "\n\n")
        self.chat.see(tk.END)

    def process(self, text):
        self.append(f"🧑 You: {text}")

        response, exit_flag = self.assistant.handle(text)

        self.append(f"🤖 Assistant: {response}")

        self.speech.speak(response)

        if exit_flag:
            self.root.destroy()

    def text_input(self):
        text = self.input.get()
        self.input.delete(0, tk.END)
        self.process(text)

    def voice_input(self):
        threading.Thread(target=self._voice_worker).start()

    def _voice_worker(self):
        self.append("Listening (speak now)...")

        text = self.speech.listen()

        if not text:
            self.append("Didn't catch that.")
            return

        self.process(text)

    def run(self):
        self.root.mainloop()