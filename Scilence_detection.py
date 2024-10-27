import os
from pydub import AudioSegment
from pydub.silence import detect_silence

# Function to calculate total speech and silence durations in a folder of audio files
def calculate_speech_and_silence_duration(folder_path, silence_threshold=-50.0, min_silence_len=1000, long_silence_len=300000):
    total_speech_duration_ms = 0  # Store the total duration of speech (non-silence) in milliseconds
    total_silence_duration_ms = 0  # Store the total duration of silence in milliseconds
    files_with_long_silence = []  # Store names of files with silence longer than 5 minutes

    # Iterate over all audio files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.wav', '.mp3', '.flac', '.ogg')):  # Add other formats if needed
            file_path = os.path.join(folder_path, filename)

            try:
                # Load the audio file
                audio = AudioSegment.from_file(file_path)

                # Detect silence in the audio
                silences = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)

                # Calculate total silence duration
                silence_duration = sum(end - start for start, end in silences)
                total_silence_duration_ms += silence_duration

                # Calculate total speech (non-silence) duration
                total_duration_ms = len(audio)
                total_speech_duration_ms += (total_duration_ms - silence_duration)

                # Check for silences longer than 5 minutes
                for start, end in silences:
                    if (end - start) > long_silence_len:
                        files_with_long_silence.append(filename)
                        break  # No need to check further for this file if a long silence is found

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Convert milliseconds to hours, minutes, and seconds for speech
    total_speech_seconds = total_speech_duration_ms / 1000
    total_speech_hours = int(total_speech_seconds // 3600)
    total_speech_minutes = int((total_speech_seconds % 3600) // 60)
    total_speech_seconds = int(total_speech_seconds % 60)

    # Convert milliseconds to hours, minutes, and seconds for silence
    total_silence_seconds = total_silence_duration_ms / 1000
    total_silence_hours = int(total_silence_seconds // 3600)
    total_silence_minutes = int((total_silence_seconds % 3600) // 60)
    total_silence_seconds = int(total_silence_seconds % 60)

    return (total_speech_hours, total_speech_minutes, total_speech_seconds), \
           (total_silence_hours, total_silence_minutes, total_silence_seconds), \
           files_with_long_silence

# Example usage
folder_path = "/Users/azizkhan/python/Spanish_audio1/"  # Updated path
speech_duration, silence_duration, files_with_long_silence = calculate_speech_and_silence_duration(folder_path)

# Print total speech and silence durations
print(f"Total speech duration: {speech_duration[0]} hours, {speech_duration[1]} minutes, {speech_duration[2]} seconds")
print(f"Total silence duration: {silence_duration[0]} hours, {silence_duration[1]} minutes, {silence_duration[2]} seconds")

# Print files with silences longer than 5 minutes
if files_with_long_silence:
    print("\nFiles with silence longer than 5 minutes:")
    for file in files_with_long_silence:
        print(f"  - {file}")
else:
    print("No files with silence longer than 5 minutes were found.")
