import os
from pydub import AudioSegment
from pydub.silence import detect_silence

# Function to remove silences longer than 5 minutes (300,000 milliseconds)
def remove_long_silences(audio_file, output_folder, silence_threshold=-50.0, min_silence_len=300000):
    # Load the audio file
    try:
        audio = AudioSegment.from_file(audio_file)
        # Detect silences in the audio longer than 5 minutes
        silences = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)

        # If there are silences longer than 5 minutes, remove them
        if silences:
            print(f"Processing file: {audio_file}")
            non_silent_audio = AudioSegment.silent(duration=0)  # Initialize an empty audio segment
            prev_end = 0

            # Process each segment that isn't silent
            for start, end in silences:
                if (end - start) > min_silence_len:
                    # Append the non-silent part before the silence
                    non_silent_audio += audio[prev_end:start]
                prev_end = end

            # Append the last part of the audio after the last silence
            non_silent_audio += audio[prev_end:]

            # Save the result to the output folder
            output_file_path = os.path.join(output_folder, os.path.basename(audio_file))
            non_silent_audio.export(output_file_path, format="wav")
            print(f"Saved processed file to: {output_file_path}")

        else:
            print(f"No silences longer than 5 minutes in: {audio_file}")

    except Exception as e:
        print(f"Error processing {audio_file}: {e}")

# Function to process multiple files
def process_audio_files(input_folder, output_folder, file_names):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output folder if it doesn't exist

    for file_name in file_names:
        audio_file_path = os.path.join(input_folder, file_name)
        remove_long_silences(audio_file_path, output_folder)

# Example usage
input_folder = "/users/azizkhan/python/Spanish_Audio"  # Folder where the original files are located
output_folder = "/users/azizkhan/python/Spanish_Audio/Output_Audio"  # Folder where the processed files will be saved

# List of files to process
file_names = [
    "LATSPAMEXTEL339.wav",
    "LATSPAMEXTEL265.wav",
    "LATSPAMEXTEL255.wav",
    "LATSPAMEXTEL252.wav",
    "LATSPAMEXTEL373.wav",
    "LATSPAMEXTEL370.wav",
    "LATSPAMEXTEL445.wav",
    "LATSPAMEXTEL481.wav",
    "LATSPAMEXTEL482.wav",
    "LATSPAMEXTEL409.wav"
]

# Process the files
process_audio_files(input_folder, output_folder, file_names)
