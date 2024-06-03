import numpy as np
import scipy.io.wavfile as wav

from pydub import AudioSegment
from scipy.signal import butter, lfilter
import os


# Noise reduction function using Butterworth filter
def butter_bandstop(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="bandstop")
    return b, a


def bandstop_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandstop(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def convert_and_clean_audio(input_file="audio.raw", output_file="audio.mp3"):
    if not os.path.exists(path=input_file):
        print("Raw file not exists.")
        return

    # Read raw audio file
    raw_audio = np.fromfile(input_file, dtype=np.int16)

    # Define sample rate and filter paramters
    sample_rate = 8000
    lowcut = 50.0
    highcut = 2400.0

    # Apply bandstop filter for noise reduction
    filtered_audio = bandstop_filter(raw_audio, lowcut, highcut, sample_rate)

    # Save filtered audio as temporary wav file
    wavfile = "temp_audio.wav"
    wav.write(wavfile, sample_rate, filtered_audio.astype(np.int16))

    # Convert wav file to mp3 using pydub
    audio = AudioSegment.from_wav(wavfile)
    audio.export("temp_audio.mp3", format="mp3")


if __name__ == "__main__":
    convert_and_clean_audio(input_file="latest.raw")
