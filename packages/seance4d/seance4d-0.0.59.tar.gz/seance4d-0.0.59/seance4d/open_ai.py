try:
    from seance4d.config import OPENAI_KEY, SYSTEM_PROMPT
except ImportError:
    from config import OPENAI_KEY, SYSTEM_PROMPT

import openai


class OpenAI:
    def __init__(self):
        ...

    @staticmethod
    def parse(text) -> str:
        """
        Parse the text using OpenAI's GPT-3 API.
        :param text: the text to parse
        :return: None
        """
        openai.my_api_key = OPENAI_KEY
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ]

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, api_key=OPENAI_KEY
        )

        reply = chat.choices[0].message.content

        return reply
