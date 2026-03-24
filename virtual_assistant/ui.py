import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from speech import SpeechEngine
from assistant import Assistant


class AssistantUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Assistant")
        self.root.geometry("640x430")
        self.root.minsize(580, 380)

        try:
            self.speech = SpeechEngine()
        except Exception as e:
            messagebox.showerror("Startup Error", str(e))
            raise

        self.assistant = Assistant()
        self.is_busy = False

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        title = ttk.Label(
            container,
            text="Voice-to-Voice Virtual Assistant",
            font=("Segoe UI", 15, "bold")
        )
        title.pack(anchor="w", pady=(0, 10))

        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = ttk.Label(container, textvariable=self.status_var, font=("Segoe UI", 10))
        status_label.pack(anchor="w", pady=(0, 10))

        note = ttk.Label(
            container,
            text="Click Listen, then speak for a few seconds.",
            font=("Segoe UI", 9)
        )
        note.pack(anchor="w", pady=(0, 10))

        user_label = ttk.Label(container, text="You said:")
        user_label.pack(anchor="w")

        self.user_box = scrolledtext.ScrolledText(container, height=5, wrap=tk.WORD, font=("Segoe UI", 10))
        self.user_box.pack(fill="x", pady=(4, 12))
        self.user_box.configure(state="disabled")

        assistant_label = ttk.Label(container, text="Assistant:")
        assistant_label.pack(anchor="w")

        self.assistant_box = scrolledtext.ScrolledText(container, height=8, wrap=tk.WORD, font=("Segoe UI", 10))
        self.assistant_box.pack(fill="both", expand=True, pady=(4, 12))
        self.assistant_box.configure(state="disabled")

        button_row = ttk.Frame(container)
        button_row.pack(fill="x")

        self.listen_btn = ttk.Button(button_row, text="Listen", command=self.start_listening)
        self.listen_btn.pack(side="left", padx=(0, 8))

        self.repeat_btn = ttk.Button(button_row, text="Repeat Last Reply", command=self.repeat_last_reply)
        self.repeat_btn.pack(side="left", padx=(0, 8))

        clear_btn = ttk.Button(button_row, text="Clear", command=self.clear_boxes)
        clear_btn.pack(side="left", padx=(0, 8))

        exit_btn = ttk.Button(button_row, text="Exit", command=self.close_app)
        exit_btn.pack(side="right")

    def set_status(self, text: str):
        self.root.after(0, lambda: self.status_var.set(f"Status: {text}"))

    def set_busy(self, busy: bool):
        self.is_busy = busy

        def update():
            self.listen_btn.config(state=("disabled" if busy else "normal"))
            self.repeat_btn.config(state=("disabled" if busy else "normal"))

        self.root.after(0, update)

    def append_user_text(self, text: str):
        def update():
            self.user_box.configure(state="normal")
            self.user_box.delete("1.0", tk.END)
            self.user_box.insert(tk.END, text)
            self.user_box.configure(state="disabled")

        self.root.after(0, update)

    def append_assistant_text(self, text: str):
        def update():
            self.assistant_box.configure(state="normal")
            self.assistant_box.delete("1.0", tk.END)
            self.assistant_box.insert(tk.END, text)
            self.assistant_box.configure(state="disabled")

        self.root.after(0, update)

    def clear_boxes(self):
        self.append_user_text("")
        self.append_assistant_text("")
        self.set_status("Idle")

    def repeat_last_reply(self):
        if self.is_busy:
            return

        last = self.assistant.last_response
        if not last:
            self.append_assistant_text("There is no previous reply to repeat.")
            return

        thread = threading.Thread(target=self._speak_only_worker, args=(last,), daemon=True)
        thread.start()

    def _speak_only_worker(self, text: str):
        self.set_busy(True)
        self.set_status("Speaking...")
        self.speech.speak(text)
        self.set_status("Idle")
        self.set_busy(False)

    def start_listening(self):
        if self.is_busy:
            return

        thread = threading.Thread(target=self._listen_and_respond_worker, daemon=True)
        thread.start()

    def _listen_and_respond_worker(self):
        self.set_busy(True)
        self.set_status("Listening...")

        user_text = self.speech.listen(duration=6)

        if not user_text:
            reply = "I couldn't hear you clearly. Please try again."
            self.append_user_text("")
            self.append_assistant_text(reply)
            self.set_status("Speaking...")
            self.speech.speak(reply)
            self.set_status("Idle")
            self.set_busy(False)
            return

        self.append_user_text(user_text)

        self.set_status("Processing...")
        response_text, should_exit = self.assistant.handle(user_text)

        self.append_assistant_text(response_text)

        self.set_status("Speaking...")
        self.speech.speak(response_text)

        if should_exit:
            self.root.after(300, self.close_app)
            return

        self.set_status("Idle")
        self.set_busy(False)

    def close_app(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()
