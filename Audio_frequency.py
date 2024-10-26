import os
from pydub import AudioSegment

def check_audio_properties(file_path, summary):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)

        # Get the number of channels
        num_channels = audio.channels
        channel_type = "Single Channel" if num_channels == 1 else "Dual Channel"

        # Get the sample rate
        sample_rate = audio.frame_rate
        if sample_rate == 8000:
            rate_type = "8 kHz"
            summary["8_kHz"] += 1
        elif sample_rate == 16000:
            rate_type = "16 kHz"
            summary["16_kHz"] += 1
        else:
            rate_type = f"{sample_rate / 1000} kHz (Other)"
        
        # Update counters
        if num_channels == 1:
            summary["single_channel"] += 1
        else:
            summary["dual_channel"] += 1

        # Print the results
        print(f"Audio File: {file_path}")
        print(f"Channel Type: {channel_type}")
        print(f"Sample Rate: {rate_type}\n")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def check_all_audio_in_folder(folder_path):
    summary = {
        "single_channel": 0,
        "dual_channel": 0,
        "8_kHz": 0,
        "16_kHz": 0
    }

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check for audio file extensions (modify as needed)
        if filename.endswith(('.wav', '.mp3', '.flac', '.ogg')):  # Add more formats if needed
            file_path = os.path.join(folder_path, filename)
            check_audio_properties(file_path, summary)
    
    # Print summary
    print("Summary of Audio Files:")
    print(f"Single Channel Files: {summary['single_channel']}")
    print(f"Dual Channel Files: {summary['dual_channel']}")
    print(f"8 kHz Files: {summary['8_kHz']}")
    print(f"16 kHz Files: {summary['16_kHz']}")

# Example usage
folder_path = "/Users/azizkhan/python/Spanish_audio1"  # Update this path
check_all_audio_in_folder(folder_path)
