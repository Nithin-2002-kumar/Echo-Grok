# EchoGrok Voice Assistant
EchoGrok is a Python-based voice assistant application powered by Grok 3, featuring a graphical user interface (GUI) built with Tkinter. It supports voice and text input, customizable themes, and user configurations stored in a JSON file. The assistant logs interactions for debugging and provides a conversational interface for user commands.
# Features

Voice and Text Input: Interact using voice commands (triggered by the hotword "echogrok") or type commands in the GUI.
Customizable Settings: Configure user name, speech rate, language, theme, and font size via echogrok_config.json.
Theming: Supports light and dark themes for the GUI.
Logging: Logs errors and interactions to echogrok.log for debugging.
Responsive GUI: Includes a scrollable chat area, input field, and buttons for listening and exiting.

# Requirements

Python 3.7 or higher
Dependencies listed in requirements.txt:pyttsx3==2.90
SpeechRecognition==3.10.0
PyAudio==0.2.14



# Installation

Clone or Download the Repository:
git clone <repository-url>
cd echogrok


Install Dependencies:
pip install -r requirements.txt

Note: On Windows, pyttsx3 requires pywin32 and comtypes for SAPI5 support. PyAudio may require additional setup for SpeechRecognition.

Ensure Files:

echogrok.py: Main application script.
echogrok_config.json: Configuration file with default settings.


Run the Application:
python echogrok.py



# Usage

Voice Commands: Say "echogrok" followed by a command (e.g., "echogrok what is the time"). The assistant responds with voice and text output.
Text Commands: Type commands in the input field and press Enter.
GUI Controls:
Listen Button (🎤): Toggles voice input.
Exit Button (❌): Closes the application with a confirmation prompt.


Configuration: Edit echogrok_config.json to customize settings like user name, speech rate, or theme.

# Configuration
The echogrok_config.json file contains:
{
    "user_name": "User",
    "speech_rate": 150,
    "preferred_language": "en",
    "theme": "light",
    "font_size": 12,
    "hotword": "echogrok"
}

# Notes

The application uses Google’s speech recognition API, requiring an internet connection for voice input.
The generate_grok_response method simulates Grok 3 responses. For real integration, use the xAI API (see https://x.ai/api).
The assistant currently handles basic commands (e.g., time, weather). Extend generate_grok_response for additional functionality.
Logs are saved to echogrok.log for debugging.

# Troubleshooting

Voice Recognition Issues: Ensure a working microphone and internet connection. Check PyAudio installation.
TTS Errors: Verify SAPI5 availability on Windows or install alternative TTS engines for other platforms.
GUI Issues: Ensure Tkinter is properly installed with your Python distribution.

# Future Enhancements

Integrate with xAI’s Grok API for real-time responses.
Add support for more commands and natural language processing.
Implement additional themes and accessibility features.

License
This project is licensed under the MIT License.
