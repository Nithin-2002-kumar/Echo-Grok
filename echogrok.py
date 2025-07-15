import logging
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import pyttsx3
import speech_recognition as sr
import json
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="echogrok.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class EchoGrokGUI:
    def __init__(self, master):
        self.master = master
        master.title("EchoGrok Voice Assistant")
        master.geometry("1000x700")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load configuration
        self.config_file = "echogrok_config.json"
        self.load_config()

        # Initialize TTS engine
        self.engine = self._init_tts_engine()

        # Recognizer for speech
        self.recognizer = sr.Recognizer()

        # GUI state variables
        self.listening = False

        # Create GUI
        self.create_widgets()

        # Initial greeting
        self.assistant_speaks(f"Hello {self.config['user_name']}! I'm EchoGrok, powered by Grok. How can I assist you today?")
        threading.Thread(target=self.listen_for_command, daemon=True).start()

    def _init_tts_engine(self):
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty("rate", self.config['speech_rate'])
            engine.setProperty("volume", 0.9)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0 if self.config['preferred_language'] == 'en' else 1].id)
            return engine
        except Exception as e:
            logging.error(f"Failed to initialize TTS engine: {e}")
            return None

    def load_config(self):
        default_config = {
            'user_name': 'User',
            'speech_rate': 150,
            'preferred_language': 'en',
            'theme': 'light',
            'font_size': 12,
            'hotword': 'echogrok'
        }
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_widgets(self):
        self.style = ttk.Style()
        self.apply_theme()

        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(expand=True, fill='both')

        self.text_area = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, state='disabled', font=('Arial', self.config['font_size']),
            bg='white', fg='black', padx=10, pady=10
        )
        self.text_area.pack(expand=True, fill='both')
        self.configure_text_tags()

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x', pady=(5, 0))
        self.command_entry = ttk.Entry(input_frame)
        self.command_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        self.command_entry.insert(0, "Type your command or use voice...")
        self.command_entry.bind("<FocusIn>", self.clear_placeholder)
        self.command_entry.bind("<FocusOut>", self.restore_placeholder)
        self.command_entry.bind("<Return>", self.process_text_command)

        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(side='left')
        self.listen_btn = ttk.Button(btn_frame, text="🎤 Listen", command=self.toggle_listening)
        self.listen_btn.pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame, text="❌ Exit", command=self.on_closing).pack(side='left')

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).pack(side='bottom', fill='x')

    def configure_text_tags(self):
        self.text_area.tag_config('user', foreground='#2c7be5', font=('Arial', self.config['font_size'], 'bold'))
        self.text_area.tag_config('assistant', foreground='#00ac69', font=('Arial', self.config['font_size']))
        self.text_area.tag_config('error', foreground='#e63757', font=('Arial', self.config['font_size']))

    def apply_theme(self):
        if self.config['theme'] == 'dark':
            self.master.config(bg='#2d2d2d')
            self.text_area.config(bg='#1e1e1e', fg='#ffffff')
            self.style.configure('TFrame', background='#2d2d2d')
            self.style.configure('TLabel', background='#2d2d2d', foreground='white')
            self.style.configure('TButton', background='#3d3d3d', foreground='white')
        else:
            self.master.config(bg='#f0f0f0')
            self.text_area.config(bg='white', fg='black')
            self.style.configure('TFrame', background='#f0f0f0')
            self.style.configure('TLabel', background='#f0f0f0', foreground='black')
            self.style.configure('TButton', background='#f0f0f0', foreground='black')

    def clear_placeholder(self, event):
        if self.command_entry.get() == "Type your command or use voice...":
            self.command_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if not self.command_entry.get():
            self.command_entry.insert(0, "Type your command or use voice...")

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_btn.config(text="🔴 Listening...")
            self.status_var.set("Listening...")
            threading.Thread(target=self.listen_for_command, daemon=True).start()
        else:
            self.listening = False
            self.listen_btn.config(text="🎤 Listen")
            self.status_var.set("Ready")

    def assistant_speaks(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"EchoGrok: {text}\n", 'assistant')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def user_says(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"You: {text}\n", 'user')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def listen_for_command(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio, language=self.config['preferred_language']).lower()
                    if self.config['hotword'] in text:
                        command = text.replace(self.config['hotword'], '').strip()
                        self.user_says(command)
                        self.get_grok_response(command)
                    else:
                        self.status_var.set("Say 'echogrok' to activate...")
                except sr.WaitTimeoutError:
                    self.status_var.set("Listening...")
                except sr.UnknownValueError:
                    self.assistant_speaks("Sorry, I didn't catch that.")
                except Exception as e:
                    logging.error(f"Listening error: {e}")
                    self.assistant_speaks("An error occurred while listening.")

    def process_text_command(self, event=None):
        command = self.command_entry.get()
        if command and command != "Type your command or use voice...":
            self.user_says(command)
            self.get_grok_response(command)
        self.command_entry.delete(0, tk.END)

    def get_grok_response(self, command):
        try:
            # Placeholder for actual Grok API integration
            grok_response = self.generate_grok_response(command)
            self.assistant_speaks(grok_response)
        except Exception as e:
            logging.error(f"Grok response error: {e}")
            self.assistant_speaks(f"Sorry, I encountered an error: {str(e)}")

    def generate_grok_response(self, command):
        if "time" in command.lower():
            return f"The current time is {datetime.now().strftime('%H:%M:%S')} on July 15, 2025. Anything else you need?"
        elif "weather" in command.lower():
            return "I don’t have real-time weather data, but I can tell you it’s always sunny when you’re talking to me! Want a joke instead?"
        elif "open" in command.lower():
            return "I can’t open apps directly, but let me know what you’re trying to open, and I’ll point you in the right direction."
        else:
            return f"You said '{command}'. Not sure what you mean, but I’m all ears—or rather, all text. What’s next?"

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit EchoGrok?"):
            self.assistant_speaks("Goodbye!")
            self.save_config()
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = EchoGrokGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Application error: {e}")
        raise
