import wave
import numpy as np
import os

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

            # Analyze channel data for differences
            channel_diff = np.mean(np.abs(audio_data[:, 0] - audio_data[:, 1]))

            if channel_diff > 0:
                print("It seems like there are different signals on each channel.")
                print(f"Difference between channels: {channel_diff}")
            else:
                print("Both channels seem to have identical audio. It might be the same speaker on both channels.")

    except wave.Error as e:
        print(f"Error processing the audio file: {e}")

# Example usage
file_path = '/users/azizkhan/python/3202NMATStereo_231005125244_5513441016-all.wav'
check_audio_channels(file_path)
