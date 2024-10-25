from pydub import AudioSegment
import csv
import os

def apply_pan_effect(audio_file, transcript_file, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract the base filename (without extension) to maintain naming
    base_filename = os.path.splitext(os.path.basename(audio_file))[0]
    
    # Define the output file path with the same base name
    output_file = os.path.join(output_folder, f"{base_filename}_stereo.wav")

    # Load the audio file
    audio = AudioSegment.from_wav(audio_file)
    audio_duration = len(audio)  # Get audio duration in milliseconds

    # Load the transcription CSV file
    with open(transcript_file, newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))

        # Calculate the duration of each segment (assuming equal division)
        segment_duration = audio_duration // len(reader)

        # Initialize new stereo audio
        new_audio = AudioSegment.silent(duration=audio_duration)  # Create silent audio for the base

        for index, row in enumerate(reader):
            speaker = row['Speaker']

            # Calculate start_time and end_time for each speaker line
            start_time = index * segment_duration
            end_time = (index + 1) * segment_duration

            # Extract the portion of the audio for the current speaker
            segment = audio[start_time:end_time]

            # Pan based on the speaker
            if speaker == "Speaker 1":
                # Pan Speaker 1 to the right ear (100% right)
                segment = segment.pan(1.0)
            elif speaker == "Speaker 2":
                # Pan Speaker 2 to the left ear (100% left)
                segment = segment.pan(-1.0)

            # Overlay this segment onto the new audio
            new_audio = new_audio.overlay(segment, position=start_time)

    # Export the new stereo audio file
    new_audio.export(output_file, format="wav")
    print(f"Stereo audio saved to {output_file}")

# Example usage
audio_file = '/users/azizkhan/python/3202NMATStereo_231005125244_5513441016-all.wav'  # Path to the original audio file
transcript_file = '/users/azizkhan/python/3202NMATStereo_231005125244_5513441016-all.csv'  # Path to the CSV transcript
output_folder = '/users/azizkhan/python/output'  # Folder where the new stereo audio will be saved

apply_pan_effect(audio_file, transcript_file, output_folder)
