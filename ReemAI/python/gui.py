import tkinter as tk
from tkinter import messagebox
import threading
import main
import voice

class ReemAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reem AI - Offline Operator")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Safety Warning
        self.warning_frame = tk.Frame(self.root, bg="#ffcccc", pady=5)
        self.warning_frame.pack(fill=tk.X)
        self.warning_label = tk.Label(
            self.warning_frame,
            text="⚠ SAFETY: This program controls your mouse and keyboard.\nUse only on systems you trust.",
            fg="red", bg="#ffcccc", font=("Arial", 10, "bold")
        )
        self.warning_label.pack()

        # Title
        self.title_label = tk.Label(self.root, text="Reem AI", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

        # Command Input Label
        self.label = tk.Label(self.root, text="What can I do for you?", font=("Arial", 12))
        self.label.pack(pady=5)

        # Command Entry
        self.command_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.command_entry.pack(pady=10)
        self.command_entry.bind("<Return>", lambda e: self.on_send())

        # Buttons Frame
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.send_btn = tk.Button(self.btn_frame, text="Send", command=self.on_send, width=10, bg="#4CAF50", fg="white")
        self.send_btn.pack(side=tk.LEFT, padx=5)

        self.voice_btn = tk.Button(self.btn_frame, text="🎤 Voice", command=self.on_voice, width=10)
        self.voice_btn.pack(side=tk.LEFT, padx=5)

        # Status Bar
        self.status_var = tk.StringVar(value="Status: Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, text):
        self.status_var.set(f"Status: {text}")

    def on_send(self):
        cmd = self.command_entry.get().strip()
        if cmd:
            self.command_entry.delete(0, tk.END)
            self.set_status("Processing command...")
            # Run in background to avoid freezing GUI
            threading.Thread(target=self.run_command, args=(cmd,), daemon=True).start()

    def run_command(self, cmd):
        try:
            main.process(cmd)
            self.root.after(0, lambda: self.set_status("Ready"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.set_status("Error occurred"))

    def on_voice(self):
        self.set_status("Listening...")
        threading.Thread(target=self.run_voice, daemon=True).start()

    def run_voice(self):
        text = voice.listen()
        if text and not text.startswith("Error"):
            self.root.after(0, lambda: self.command_entry.insert(0, text))
            self.root.after(0, lambda: self.set_status("Voice recognized"))
        else:
            self.root.after(0, lambda: self.set_status(text if text else "Could not hear anything"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ReemAIApp(root)
    root.mainloop()
