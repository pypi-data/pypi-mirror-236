import subprocess
import threading
from importlib import resources as impresources

from gtts import gTTS


class TextToSpeech:
    @staticmethod
    def speak_reply(stopped: threading.Event, reply, text_parser):
        language = "en"

        try:
            # use Google Text to Speech
            TextToSpeech.generate_text(text=reply, language=language)

            TextToSpeech.playback(stopped=stopped, text_parser=text_parser)
        except Exception as e:
            TextToSpeech.playback(
                stopped=stopped, text_parser=text_parser, filename="error.mp3"
            )

    @staticmethod
    def playback(
        stopped: threading.Event,
        text_parser,
        filename="response.mp3",
    ):
        # determine if filename exists
        try:
            with open(filename):
                pass
        except FileNotFoundError:
            print(f"Could not find {filename}. Trying local.")
            inp_file = impresources.files("seance4d") / filename

            filename = str(inp_file)
            print(f"Remapped to: {filename}")

        if stopped is not None:
            stopped.clear()

        if text_parser is not None:
            text_parser.reset()

        subprocess.call(
            ["mpg321", filename],
            bufsize=4096,
            stdout=None,
            stderr=None,
        )

        if stopped is not None:
            print("Flag cleared and listening process restarted")
            stopped.set()

    @staticmethod
    def generate_text(text, language="en", output_file="response.mp3"):
        gTTS(text=text, lang=language, slow=False).save(output_file)
