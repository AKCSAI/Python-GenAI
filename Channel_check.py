import wave
import numpy as np
import os
from scipy.fft import fft

def check_audio_channels(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"The file at {file_path} does not exist.")
        return

    # Open the wave file
    try:
        with wave.open(file_path, 'rb') as wav_file:
            # Get parameters
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()

            print(f"Audio File Info:")
            print(f" - Channels: {n_channels}")
            print(f" - Sample Width: {sample_width} bytes")
            print(f" - Frame Rate: {framerate} Hz")
            print(f" - Total Frames: {n_frames}")

            if n_channels < 2:
                print("This is a mono file. There are no multiple channels to compare.")
                return

            # Read the audio frames and convert to numpy array for processing
            frames = wav_file.readframes(n_frames)
            audio_data = np.frombuffer(frames, dtype=np.int16)

            # Reshape the array into channels
            audio_data = np.reshape(audio_data, (-1, n_channels))

            # Perform FFT for each channel
            left_channel_fft = np.abs(fft(audio_data[:, 0]))[:n_frames // 2]
            right_channel_fft = np.abs(fft(audio_data[:, 1]))[:n_frames // 2]

            # Normalize the FFT output to compare them more easily
            left_channel_fft /= np.max(left_channel_fft)
            right_channel_fft /= np.max(right_channel_fft)

            # Compute the mean absolute difference between the FFT results of the two channels
            fft_diff = np.mean(np.abs(left_channel_fft - right_channel_fft))

            # Threshold to determine if sound signatures are distinct
            if fft_diff > 0.1:  # You can adjust this threshold based on your requirements
                print(f"The channels have distinct sound signatures with a difference of {fft_diff}.")
            else:
                print(f"The channels have very similar sound signatures with a difference of {fft_diff}.")

    except wave.Error as e:
        print(f"Error processing the audio file: {e}")

# Example usage with your file path
file_path = '/users/azizkhan/python/3202NMATStereo_231005125244_5513441016-all.wav'
check_audio_channels(file_path)

