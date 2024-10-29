import os
import wave
import numpy as np

# Function to check if a stereo file's channels are identical
def check_if_stereo_is_mono(filepath):
    with wave.open(filepath, 'rb') as wav_file:
        if wav_file.getnchannels() != 2:
            # Not a stereo file
            return False
        
        # Read frames and convert them to a numpy array
        frames = wav_file.readframes(-1)
        samples = np.frombuffer(frames, dtype=np.int16)
        
        # Separate left and right channels
        left_channel = samples[0::2]
        right_channel = samples[1::2]
        
        # Compare the two channels
        return np.array_equal(left_channel, right_channel)

# Function to analyze all WAV files in the folder
def analyze_audio_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            if check_if_stereo_is_mono(file_path):
                print(f"The file '{file_name}' is likely converted from mono to stereo.")
            else:
                print(f"The file '{file_name}' has distinct stereo channels.")

# Folder containing audio files
audio_folder = '/Users/azizkhan/python/Test_Files'

# Analyze the files
analyze_audio_files(audio_folder)
