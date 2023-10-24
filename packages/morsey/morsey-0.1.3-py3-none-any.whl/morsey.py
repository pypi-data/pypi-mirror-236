"""
Contains all morsey methods. Functionalities involve translating english and morse code in various mediums.
"""
import wavio
import numpy as np
from playsound import playsound

def morse_text_to_english_text(code: str) -> str:
    """
    Translates morse code text to English text.

    This is a git test

    Parameters:
        code (str): Morse code string to be translated.

    Returns:
        str: Translated English text.

    Example:
        >>> morse_code = "... --- ... / --- ... ---"
        >>> english_text = morse_text_to_english_text(morse_code)
        >>> print(english_text)
        "SOS OSO"
    """
    morse_code_dict_reversed = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z',
        '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
        '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
        '/': ' ',
        '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!',
        '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
        '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
        '.-..-.': '"', '...-..-': '$', '.--.-.': '@',
        # You can add more Morse code characters as needed.
    }

    if type(code) != str:
        raise TypeError("Input must be of type str")

    # Split input code into list of 'char' strings
    code_split = code.split(' ')

    english_text = ""

    # Translate each 'char' and append to output string.
    for char in code_split:
        english_text += morse_code_dict_reversed[char]

    return english_text


def english_text_to_morse_text(english_text: str) -> str:
    """
    Translates English text to morse code text.

    Parameters:
        english_text (str): English text to be translated.

    Returns:
        str: Translated Morse code text.

    Example:
        >>> english_text = "SOS OSO"
        >>> morse_code = english_text_to_morse_text(english_text)
        >>> print(morse_code)
        "... --- ... / --- ... ---"
    """

    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        ' ': '/',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
        '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
        ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
        '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    }

    if type(english_text) != str:
        raise TypeError("Input must be of type str")

    english_text = english_text.upper()

    # Translate each 'char' and append to output string.
    code = ""
    for char in english_text:
        code += (morse_code_dict[char] + " ")

    code = code.rstrip(' ')
    return code


def morse_text_to_audio(
        morse: str, time: float, filename: str, play=False, rate=22050, frequency=600.0,
        unit_fade_percent=0.01) -> None:
    """
    Creates a .wav file representation of the inputted morse string.

    :param morse: Morse code str to be converted into .wav file
    :param rate: Samples per second
    :param time: Length of created file (seconds)
    :param frequency: Steady frequency of morse code tones.
    :param filename: filename of output .wav file
    :param play: If True, will use playsound to play created audio file.
    :param unit_fade_percent: Percentage of unit "beep" to be faded for popping reduction.
    :return: Returns None, creates a .wav file
    """

    # n = total number of samples to be taken
    n = int(rate * time)

    sound_array = np.zeros(n)

    # Finds correct unit length to accurately fit all morse code in 'time'
    # "-. .. / .-" takes 3 + 1 + 3 + 1 + 1 + 3 + 1 + 3 + 1 + 3 for the chars alone
    # Chars are separated by 1 unit and have an extra unit at the end for concatenation purposes
    units = 0
    for char in morse:
        if char == '-':
            units += 4
        else:
            units += 2

    def fade(array: np.array, fade_percent: float):
        """
    Apply a fade-in and fade-out effect to the start and end of a given audio waveform.

    This function modifies the audio waveform by gradually reducing the volume at the
    beginning and end to prevent popping or clicking noises during playback or
    concatenation.

    Parameters:
        array (np.array): A one-dimensional numpy array representing an audio waveform.
        fade_percent (float): The percentage of the waveform to fade at the start and end.
            A value between 0 and 0.5 is recommended for best results.

    Returns:
        np.array: A numpy array representing the audio waveform with the fade effect applied.

    The fade effect is applied by linearly transitioning the volume from 0 to the original
    amplitude over the specified percentage of the waveform at both the beginning and end.
    """
        if fade_percent >= 0.5:
            raise ValueError("Percent must be less than 0.5")

        size = array.shape
        fade_size = int(fade_percent * size[0])

        fade_line = np.linspace(0, 1, num=fade_size)
        array[0:fade_size] = array[0:fade_size] * fade_line

        array[-1 * (fade_size + 1):-1] = array[-1 * (fade_size + 1):-1] * fade_line[::-1]

        return array

    # unit_wave is the sine wave representing the body of one unit of "beeping" morse code. Unit length is trimmed so
    # that unit_wave ends at a full cycle of the sine function i.e. the last values approach 0 from the negative.
    # Fade function reduces popping by gradually transitioning from 0 sound to full frequency.

    unit_length = n // units

    unit_wave = np.sin(2 * np.pi * frequency * np.arange(unit_length) / rate)
    zeros = (np.where(abs(unit_wave) <= 0.01)[0])
    unit_wave = unit_wave[:zeros[-1] + 1]
    unit_wave[-1] = 0
    unit_length = unit_wave.size
    unit_wave = fade(unit_wave, unit_fade_percent)

    three_unit_wave = np.sin(2 * np.pi * frequency * np.arange(3 * unit_length) / rate)
    zeros = np.where(abs(three_unit_wave) <= 0.01)[0]
    three_unit_wave = three_unit_wave[:zeros[-1] + 1]
    three_unit_wave[-1] = 0
    three_unit_length = three_unit_wave.size
    three_unit_wave = fade(three_unit_wave, unit_fade_percent / 3.0)

    # Iterates over 'morse', adding a dot, dash, or break sound to the numpy array.
    index = 0
    for char in morse:
        if char == '.':
            sound_array[index:index + (1 * unit_length)] = unit_wave
            index += 1 * unit_length
        elif char == '-':
            sound_array[index:index + three_unit_length] = three_unit_wave
            index += 3 * unit_length
        elif char == ' ':
            index += 1 * unit_length
        elif char == '/':
            index += 1 * unit_length
        else:
            raise SyntaxError("Morse str must only contain ['.', '-', ' ', '/']")

        index += 1 * unit_length

    if not filename.endswith(".wav"):
        raise SyntaxError("File must be of type .wav")

    try:
        file = open(filename, 'wb')
    except FileNotFoundError:
        file = open(filename, 'xb')

    wavio.write(file, sound_array, rate, sampwidth=2)

    if play:
        playsound(filename)

    file.close()
