import os
from pydub.utils import mediainfo
from pydub import AudioSegment

# Function to get the duration of an audio file
def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000  # Returns duration in seconds

# Function to get total duration of all audio files in the folder
def total_audio_duration(folder_path):
    total_duration = 0
    for filename in os.listdir(folder_path):
        if filename.endswith((".wav", ".mp3", ".flac", ".ogg")):  # Add other extensions if needed
            file_path = os.path.join(folder_path, filename)
            try:
                duration = get_audio_duration(file_path)
                total_duration += duration
            except Exception as e:
                print(f"Could not process file {filename}: {e}")
    return total_duration

# Define the folder path
folder_path = "/Users/azizkhan/python/Spanish_audio1"

# Get the total audio duration
total_duration = total_audio_duration(folder_path)

# Convert the total duration to hours, minutes, and seconds
hours = int(total_duration // 3600)
minutes = int((total_duration % 3600) // 60)
seconds = int(total_duration % 60)

print(f"Total audio duration: {hours} hours, {minutes} minutes, {seconds} seconds")
