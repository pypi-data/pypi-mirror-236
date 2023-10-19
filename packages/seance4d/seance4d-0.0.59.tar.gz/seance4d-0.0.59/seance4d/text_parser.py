import json

try:
    from seance4d.config import GOOGLE_KEY
except ImportError:
    from config import GOOGLE_KEY

import os
from importlib import resources as impresources

import speech_recognition as sr
from rich.pretty import pprint as print


class TextParser:
    def __init__(
        self,
        prompt_text="greetings",
        end_text="hear me",
        end_program_text="end program",
        shutdown_text="stop it now",
    ):
        self.prompt_text = prompt_text
        self.shutdown_text = shutdown_text
        self.end_text = end_text
        self.end_program_text = end_program_text
        self.found_prompt = False
        self.is_ready = False
        self.buffer = ""
        self.cached_filename = ""

    def reset(self):
        self.__init__(prompt_text=self.prompt_text, end_text=self.end_text)

    def parse(self, filename="output.wav"):
        r = sr.Recognizer()

        with sr.AudioFile(filename) as source:
            # convert from speech to text
            try:
                text = r.recognize_google(r.record(source), key=GOOGLE_KEY)

                self._handle_text(text)
            except sr.UnknownValueError:
                print(f"Ditching indecipherable text")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech "
                    f"Recognition service; {e}"
                )

    def _handle_text(self, text):
        """
        Handle the text that has been parsed from the audio.
        :param text: the text to handle
        :return: None
        """

        # detect whether this is a cache entry
        is_cached, filename, response = self._is_cached(text)

        if is_cached:
            print(f"Found cached response: {filename}")
            self.buffer = response
            self.cached_filename = f"cached_{filename}"
            self.is_ready = True
            return

        if self.end_program_text.lower() in text.lower():
            print(f"End program command received")
            self.buffer = ""
            self.is_ready = False
            os._exit(0)

        if self.shutdown_text.lower() in text.lower():
            print(f"Shutdown command received")
            self.buffer = ""
            self.is_ready = False
            os.system("shutdown -h now")

        if not self.found_prompt and self.prompt_text.lower() in text.lower():
            # if we haven't found the prompt yet, and we find it
            print(f"Starting with {text}")

            self.found_prompt = True
            self.buffer = text.lower().split(self.prompt_text.lower())[1]
            text = text.lower().split(self.prompt_text.lower())[1]

        if self.found_prompt and self.end_text.lower() in text.lower():
            # if we have found the prompt, and we find the end text
            print(f"Ending with {text}")
            self.buffer += text.lower().split(self.end_text.lower())[0]
            self.is_ready = True

        elif self.found_prompt:
            # if we have found the prompt, and we haven't found the
            # end text
            print(f"Appending {text}")
            self.buffer += text

        else:
            # if we haven't found the prompt yet, and we haven't found
            # the end text
            print(f"Audio discarded: {text}")

    def _is_cached(self, text: str):
        filename = "cached.json"

        text_to_use: str = text.lower().replace(self.prompt_text, "")
        text_to_use = text_to_use.replace(self.end_text, "")
        text_to_use = text_to_use.replace("alicia ", "")
        text_to_use = text_to_use.replace("please ", "")
        text_to_use = text_to_use.replace("  ", " ")
        text_to_use = text_to_use.strip()

        print(f"Checking cached comparator text: {text_to_use}")

        # locate the cache file
        try:
            with open(filename):
                pass
        except FileNotFoundError:
            print(f"Could not find {filename}. Trying local.")
            inp_file = impresources.files("seance4d") / filename

            filename = str(inp_file)
            print(f"Remapped to: {filename}")

        # load the cache file and search for the text
        with open(filename, "r") as json_file:
            json_data = json.load(json_file)

            for item in json_data:
                count = [
                    (w, item["question"].split(" ").count(w))
                    for w in set(item["question"].split(" "))
                    if w in text_to_use
                ]

                if (
                    len(count) > 3
                    and len(count) >= len(set(text_to_use.split(" "))) - 2
                ):
                    # "we got one!"
                    return True, item["file"], item["response"]

        # no dice
        return False, "", ""
