import json
import sys
import threading
import wave
from array import array
from queue import Queue, Full
import random

import alsaaudio
import click
from rich.pretty import pprint as print

try:
    from seance4d.open_ai import OpenAI
    from seance4d.text_parser import TextParser
    from seance4d.text_to_speech import TextToSpeech
    from seance4d.config import MIN_VOL
except ImportError:
    from open_ai import OpenAI
    from text_parser import TextParser
    from text_to_speech import TextToSpeech
    from config import MIN_VOL

CHUNK_SIZE: int = 4096
MIN_VOLUME: int = MIN_VOL
BUF_MAX_SIZE: int = CHUNK_SIZE * 100

CHANNELS: int = 1
INPUT_FORMAT: int = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE: int = 44100
FRAME_SIZE: int = 1024

OUTPUT_WAV: str = "output.wav"

# default text parser
text_parser: TextParser = TextParser(
    prompt_text="greetings", end_text="hear me"
)


def main(threshold: bool = False, verbose_mode: bool = False) -> None:
    """
    Main function for the program
    :param threshold: whether to display threshold volume information
    :param verbose_mode: whether to display verbose information
    :return: None
    """
    # load welcome vocal
    TextToSpeech.playback(
        stopped=None, text_parser=None, filename="welcome.mp3"
    )

    stopped: threading.Event = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))

    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(
        target=record, args=(stopped, q, threshold, verbose_mode)
    )
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


def record(
    stopped: threading.Event, q: Queue, threshold: bool, verbose_mode: bool
) -> None:
    """
    Record the audio data
    :param stopped: the stopped signal
    :param q: the queue to put the audio data into
    :param threshold: whether to display threshold volume information
    :param verbose_mode: whether to display verbose information
    :return: None
    """
    (
        current_fail_count,
        current_voice_count,
        filename,
        silence_count,
        wf,
    ) = set_variables()

    while True:
        if stopped.wait(timeout=0):
            pass

        chunk = q.get()

        current_fail_count, current_voice_count = check_voice_volume(
            current_fail_count,
            current_voice_count,
            chunk,
            wf,
            threshold,
            verbose_mode,
        )

        current_fail_count, current_voice_count, wf = check_success(
            current_fail_count,
            current_voice_count,
            silence_count,
            stopped,
            wf,
            verbose_mode,
        )


def check_success(
    current_fail_count,
    current_voice_count,
    silence_count,
    stopped,
    wf,
    verbose_mode,
):
    """
    Check if the voice has been silent for long enough to close the file
    :param current_fail_count: the current fail count
    :param current_voice_count: the current voice count
    :param silence_count: the silence count
    :param stopped: the stopped signal
    :param wf: the wave file
    :param verbose_mode: whether to display verbose information
    :return: the current fail count, the current voice count, and the wave file
    """
    if current_fail_count > silence_count and current_voice_count > 1:
        if verbose_mode:
            print("Closing file")

        wf.close()

        current_fail_count = 0
        current_voice_count = 0

        text_parser.parse(filename=OUTPUT_WAV)

        if text_parser.is_ready:
            if stopped is not None:
                stopped.set()

            if text_parser.cached_filename != "":
                print(f"ChatGPT cached: {text_parser.buffer}")
                text_parser.buffer = ""

                TextToSpeech.playback(
                    stopped=stopped,
                    text_parser=text_parser,
                    filename=text_parser.cached_filename,
                )

                text_parser.cached_filename = ""
            else:
                try:
                    TextToSpeech.playback(
                        stopped=stopped,
                        text_parser=None,
                        filename=f"Hmm{random.randint(1, 3)}.mp3",
                    )

                    ai_response = OpenAI.parse(text_parser.buffer)
                    print(f"ChatGPT: {ai_response}")

                    TextToSpeech.playback(
                        stopped=stopped,
                        text_parser=None,
                        filename="holding.mp3",
                    )

                    TextToSpeech.speak_reply(
                        stopped=stopped,
                        reply=ai_response,
                        text_parser=text_parser,
                    )
                except Exception as e:
                    # playback an error file
                    TextToSpeech.playback(
                        stopped=stopped,
                        text_parser=text_parser,
                        filename="error.mp3",
                    )

        # reset the wave file
        (
            _,
            _,
            filename,
            _,
            wf,
        ) = set_variables()

        if stopped is not None:
            stopped.clear()

    return current_fail_count, current_voice_count, wf


def set_variables():
    """
    Set the variables for the program and reopen the wave file
    :return: the current fail count, the current voice count, the filename,
     the silence count, and the wave file
    """
    current_fail_count = 0
    current_voice_count = 0
    silence_count = 50
    filename = OUTPUT_WAV
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setframerate(44100)
    wf.setsampwidth(2)
    return current_fail_count, current_voice_count, filename, silence_count, wf


def check_voice_volume(
    current_fail_count,
    current_voice_count,
    chunk,
    wf,
    threshold: bool,
    verbose_mode: bool,
):
    """
    Check the volume of the voice
    :param current_fail_count: the current fail count
    :param current_voice_count: the current voice count
    :param chunk: the chunk of audio data
    :param wf: the wave file
    :param threshold: whether to display threshold volume information
    :param verbose_mode: whether to display verbose information
    :return: the current fail count and the current voice count
    """
    vol = max(chunk)

    if threshold:
        print(f"Volume: {vol}")

    if vol >= MIN_VOLUME:
        current_fail_count = 0

        if verbose_mode:
            print("Sound detected: writing chunk")

        wf.writeframesraw(chunk)
        current_voice_count += 1
    else:
        if current_voice_count == 0:
            current_fail_count = 0
        else:
            if verbose_mode:
                print("Mid-voice silence detected: writing chunk")

            wf.writeframesraw(chunk)
            current_fail_count += 1
    return current_fail_count, current_voice_count


def listen(stopped, q) -> None:
    """
    The initial listener thread
    :param stopped: a signal to start and stop listening to avoid feedback
    :param q: the queue to put the audio data into
    :return: None
    """
    print("Available devices:")
    print(alsaaudio.cards())

    try:
        indices = [
            (device_number, card_name)
            for device_number, card_name in enumerate(alsaaudio.cards())
            if "C930e" in card_name or "Device" in card_name
        ]

        print("Using device:")
        print(indices[0])

    except OSError:
        print("No device found")
        sys.exit(1)
    except IndexError:
        print("No device found")
        sys.exit(1)

    # set up audio input
    recorder = alsaaudio.PCM(
        type=alsaaudio.PCM_CAPTURE,
        channels=CHANNELS,
        rate=RATE,
        format=INPUT_FORMAT,
        periodsize=FRAME_SIZE,
        device=f"hw:{indices[0][0]}",
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(array("h", recorder.read()[1]))
        except Full:
            pass  # discard


@click.command()
def threshold_test():
    """
    Run in threshold test mode
    """
    main(threshold=True)


@click.command()
def run() -> None:
    """
    Run in normal mode
    """
    main(threshold=False)


@click.command()
def verbose() -> None:
    """
    Run in verbose mode
    """
    main(verbose_mode=True)


@click.command()
@click.argument("text")
def generate_speech(text) -> None:
    """
    Generate a block of speech. For making pre-formed responses.
    """
    TextToSpeech.generate_text(text=text, output_file="pregenerated.mp3")


@click.command()
@click.argument("prompt")
def test_prompt(prompt) -> None:
    """
    Test a prompt and give the ChatGPT response
    """
    text_parser._handle_text(prompt)

    if text_parser.is_ready:
        if text_parser.cached_filename != "":
            print(f"ChatGPT cached: {text_parser.buffer}")
            text_parser.buffer = ""

            TextToSpeech.playback(
                stopped=None,
                text_parser=None,
                filename=text_parser.cached_filename,
            )

            text_parser.cached_filename = ""
        else:
            try:
                TextToSpeech.playback(
                    stopped=None,
                    text_parser=None,
                    filename=f"Hmm{random.randint(1, 3)}.mp3",
                )

                ai_response = OpenAI.parse(text_parser.buffer)
                print(f"ChatGPT: {ai_response}")

                TextToSpeech.playback(
                    stopped=None,
                    text_parser=None,
                    filename="holding.mp3",
                )

                TextToSpeech.speak_reply(
                    stopped=None,
                    reply=ai_response,
                    text_parser=text_parser,
                )
            except Exception as e:
                # playback an error file
                TextToSpeech.playback(
                    stopped=None,
                    text_parser=text_parser,
                    filename="error.mp3",
                )
    else:
        print(
            f"Command not recognised. Perhaps you "
            f"needed {text_parser.prompt_text} QUERY {text_parser.end_text}?"
        )


@click.command()
@click.argument("input_file")
def augment_cache(input_file) -> None:
    """
    Add ChatGPT responses to a cache file
    """
    with open(input_file, "r") as json_file:
        json_data = json.load(json_file)

        for item in json_data:
            try:
                ai_response = OpenAI.parse(item["question"])
                item["response"] = ai_response
            except Exception as e:
                print(f"Error: {e}")
                item["response"] = "ERROR"

    with open(input_file, "w") as json_file:
        json.dump(json_data, json_file)


@click.command()
@click.argument("input_file")
def generate_cache_speech(input_file) -> None:
    """
    Create speech files for each entry in a cache file
    """
    with open(input_file, "r") as json_file:
        json_data = json.load(json_file)

        for item in json_data:
            try:
                TextToSpeech.generate_text(
                    text=item["response"], output_file=f"cached_{item['file']}"
                )
                print(f"Generated {item['file']}")
            except Exception as e:
                print(f"Error generating {item['file']}: {e}")


@click.command()
def test_error() -> None:
    """
    Test error handling
    """
    TextToSpeech.playback(stopped=None, text_parser=None, filename="error.mp3")


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(augment_cache)
    cli.add_command(generate_cache_speech)
    cli.add_command(generate_speech)
    cli.add_command(run)
    cli.add_command(test_error)
    cli.add_command(test_prompt)
    cli.add_command(threshold_test)
    cli.add_command(verbose)
    cli()
