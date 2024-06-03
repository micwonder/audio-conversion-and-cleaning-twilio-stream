# Audio Conversion and Cleaning

This repository provides a Python script to convert raw audio data to MP3 format while reducing noise. It utilizes the Twilio Media Stream over WebSocket to receive audio data and applies noise reduction techniques to enhance the audio quality.

## Features

- Decodes raw audio data from base64 encoding.
- Applies a Butterworth bandstop filter for noise reduction.
- Converts cleaned audio to WAV format using the `pywav` library.
- Converts the WAV file to MP3 format using the `pydub` library.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `numpy`
  - `scipy`
  - `pydub`
  - `pywav`
  - `audioop`

You can install the required packages using pip:

```bash
pip install numpy scipy pydub pywav audioop
```

## Usage

1. **Save the raw audio data:**

   The `save_audio_data` function saves the base64-encoded audio payload to a raw audio file.

   ```python
   def save_audio_data(media_payload, output_file='audio.raw'):
       audio_data = base64.b64decode(media_payload)
       with open(output_file, 'ab') as file:
           file.write(audio_data)
   ```

2. **Convert and clean the audio:**

   The `convert_and_clean_audio` function converts the raw audio file to MP3 format while reducing noise.

3. **Run the script:**

   To convert and clean the audio, simply run the script:

   ```bash
   python convert_and_clean_audio.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Twilio Media Streams](https://www.twilio.com/docs/voice/tutorials/consume-real-time-media-stream-using-websockets-python-and-flask) for providing the initial code for handling WebSocket connections.
- [pydub](https://pydub.com/) for audio file format conversions.
- [pywav](https://github.com/hbldh/pywav) for better handling of WAV files.
