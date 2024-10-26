import os
from pydub import AudioSegment
import hashlib

# Function to generate a hash for the audio file content
def generate_audio_hash(file_path):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        # Convert the audio to raw data and create a hash of the content
        audio_data = audio.raw_data
        return hashlib.md5(audio_data).hexdigest()
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def find_duplicates(folder_path):
    name_duplicates = {}
    sound_duplicates = {}
    sound_signatures = {}

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.wav', '.mp3', '.flac', '.ogg')):  # Modify as needed
            file_path = os.path.join(folder_path, filename)

            # Check for name-based duplicates
            if filename in name_duplicates:
                name_duplicates[filename].append(file_path)
            else:
                name_duplicates[filename] = [file_path]

            # Check for sound-signature based duplicates
            audio_hash = generate_audio_hash(file_path)
            if audio_hash:
                if audio_hash in sound_signatures:
                    sound_signatures[audio_hash].append(file_path)
                else:
                    sound_signatures[audio_hash] = [file_path]

    # Filter to keep only actual name duplicates
    name_duplicates = {k: v for k, v in name_duplicates.items() if len(v) > 1}

    # Filter to keep only actual sound duplicates
    sound_duplicates = {k: v for k, v in sound_signatures.items() if len(v) > 1}

    return name_duplicates, sound_duplicates

def print_duplicate_summary(name_duplicates, sound_duplicates):
    total_name_duplicates = sum(len(v) - 1 for v in name_duplicates.values())
    total_sound_duplicates = sum(len(v) - 1 for v in sound_duplicates.values())

    # Print name-based duplicates
    if name_duplicates:
        print(f"Number of name-based duplicate files: {total_name_duplicates}")
        for name, files in name_duplicates.items():
            print(f"\nDuplicate name: {name}")
            for file in files:
                print(f"  - {file}")
    else:
        print("No name-based duplicate files found.")

    # Print sound-signature-based duplicates
    if sound_duplicates:
        print(f"\nNumber of sound-based duplicate files: {total_sound_duplicates}")
        for audio_hash, files in sound_duplicates.items():
            print(f"\nDuplicate sound signature (hash: {audio_hash}):")
            for file in files:
                print(f"  - {file}")
    else:
        print("No sound-signature-based duplicate files found.")

# Example usage
folder_path = "/Users/azizkhan/python/Spanish_audio1"  # Update this path

# Find duplicates
name_duplicates, sound_duplicates = find_duplicates(folder_path)

# Print the results
print_duplicate_summary(name_duplicates, sound_duplicates)
