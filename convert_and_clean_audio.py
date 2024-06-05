import matplotlib.pyplot as plt
import numpy as np

# import scipy.io.wavfile as wav

# import audioop
from scipy.signal import resample

from pywav import WavWrite

from pydub import AudioSegment
from scipy.signal import butter, lfilter, welch
import os


# Noise reduction function using Butterworth filter
def butter_bandstop(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(
        order, [low, high], btype=["lowpass", "highpass", "bandpass", "bandstop"][3]
    )
    return b, a


def bandstop_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandstop(lowcut, highcut, fs, order=order)
    print(b, a)
    y = lfilter(b, a, data)
    return y


def truncate_audio(audio_data, sample_rate, duration_ms):
    num_samples = int(sample_rate * (duration_ms / 1000))
    return audio_data[num_samples:]


def visualize(data, figure_number=1):
    length = len(data)
    # time = np.linspace(0, 1, num=length)
    time = np.arange(0, int(length), 1)
    print()

    plt.figure(figure_number)
    plt.title("Sound Wave")
    plt.xlabel("Time")
    plt.plot(
        time,
        data[: int(length)],
    )

    # plt.ylim(-64000, 64000)


def combine_chunks(
    high_freq,
    low_freq,
    fs,
    threshold=1e-5,
    f_cutoff=1000,
    max_value=np.iinfo(np.int8).max / 1.1,
):
    high_freq[high_freq > max_value] = -2
    low_freq[low_freq > max_value] = -2
    high_freq = high_freq.astype(np.int16)
    low_freq = low_freq.astype(np.int16)
    combined = ((high_freq + low_freq) // 2).astype(np.int8)
    return combined
    # return np.maximum(high_freq, low_freq)
    # return low_freq


def combine_chunks(
    high_freq,
    low_freq,
    fs,
    threshold=1e-5,
    f_cutoff=1000,
    max_value=np.iinfo(np.int8).max / 1.1,
):
    high_freq[high_freq > max_value] = -2
    low_freq[low_freq > max_value] = -2
    freqs_high, psd_high = welch(high_freq, fs=fs)
    freqs_low, psd_low = welch(low_freq, fs=fs)
    has_voice = np.max(psd_high[freqs_high <= f_cutoff]) > threshold
    combined = high_freq if has_voice else low_freq
    combined[combined > max_value] = max_value
    return combined


def remove_repetitive_chunks(audio_data, chunk_size=160, fs=8000):
    unique_chunks = []
    print(len(audio_data))
    visualize(audio_data)
    empty_list = np.full(chunk_size, -2, dtype=np.int8)
    # print(audio_data[0:chunk_size])

    for i in range(0, len(audio_data), chunk_size * 2):
        chunk_high_freq = audio_data[i : i + chunk_size]
        chunk_low_freq = audio_data[i + chunk_size : i + chunk_size * 2]
        # if len(unique_chunks) == 0 or chunk != unique_chunks[-320:]:
        #     unique_chunks.append(chunk)
        unique_chunks.append(combine_chunks(chunk_high_freq, chunk_low_freq, fs))
        # None

    return np.concatenate(unique_chunks)
    # return unique_chunks
    # visualize(enh_data, 2)


def convert_and_clean_audio(input_file="audio.raw", output_file="audio.mp3"):
    if not os.path.exists(path=input_file):
        print("Raw file not exists.")
        return

    # Read raw audio file
    raw_audio = np.fromfile(input_file, dtype=np.int8)

    # Define sample rate and filter paramters
    sample_rate = 8000
    lowcut = 500.0
    highcut = 1250.0

    # Truncate the first 100 milliseconds
    # truncated_audio = truncate_audio(raw_audio, sample_rate, 100)

    # Resample the audio data to the target sample rate and apply bandstop filter for noise reduction
    # num_samples = int(len(raw_audio) * (8000 / sample_rate))
    # resampled_audio = resample(raw_audio, num_samples)
    # filtered_audio = bandstop_filter(raw_audio, lowcut, highcut, sample_rate)
    # filtered_audio = audioop.ulaw2lin(raw_audio, 1)
    filtered_audio = raw_audio

    # Remove repetitive chunks
    cleaned_audio = remove_repetitive_chunks(filtered_audio)
    print(cleaned_audio.shape)
    print(len(cleaned_audio))
    visualize(cleaned_audio)
    plt.show()
    # cleaned_audio = resampled_audio

    filtered_audio = cleaned_audio

    # Write to WAV file using pywav
    wavfile = "temp_audio.wav"
    wav_write = WavWrite(wavfile, 1, sample_rate, 16, 7)
    wav_write.write(filtered_audio.tobytes())
    wav_write.close()

    # Convert wav file to mp3 using pydub
    audio = AudioSegment.from_file(wavfile, "wav")
    audio = audio.set_frame_rate(16000).set_sample_width(1).set_channels(1)
    audio.export("temp_audio.mp3", format="mp3")


if __name__ == "__main__":
    convert_and_clean_audio(input_file="audio (2).raw")
