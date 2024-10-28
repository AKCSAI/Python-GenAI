import os
from pydub import AudioSegment
import hashlib

# Function to generate a hash for the audio file content
def generate_audio_hash(file_path):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        # Get audio duration
        duration = len(audio) / 1000  # Convert to seconds
        # Convert the audio to raw data and create a hash of the content
        audio_data = audio.raw_data
        return hashlib.md5(audio_data).hexdigest(), duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

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
            audio_hash, duration = generate_audio_hash(file_path)
            if audio_hash:
                if duration not in sound_signatures:
                    sound_signatures[duration] = {}  # Group by duration first
                if audio_hash in sound_signatures[duration]:
                    sound_signatures[duration][audio_hash].append(file_path)
                else:
                    sound_signatures[duration][audio_hash] = [file_path]

    # Filter to keep only actual name duplicates
    name_duplicates = {k: v for k, v in name_duplicates.items() if len(v) > 1}

    # Filter to keep only actual sound duplicates
    sound_duplicates = {duration: files for duration, hashes in sound_signatures.items()
                        for audio_hash, files in hashes.items() if len(files) > 1}

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
        for duration, files in sound_duplicates.items():
            print(f"\nDuplicate sound files with duration ~ {duration} seconds:")
            for file in files:
                print(f"  - {file}")
    else:
        print("No sound-signature-based duplicate files found.")

# Example usage
folder_path = "/Users/azizkhan/python/Test1/Spanishaudio"  # Update this path

# Find duplicates
name_duplicates, sound_duplicates = find_duplicates(folder_path)

# Print the results
print_duplicate_summary(name_duplicates, sound_duplicates)