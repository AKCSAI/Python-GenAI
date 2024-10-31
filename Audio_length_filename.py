import os
from pydub.utils import mediainfo
from openpyxl import Workbook

def get_audio_duration(file_path):
    """Get the duration of an audio file and return it in HH:MM:SS format."""
    try:
        info = mediainfo(file_path)
        duration = float(info['duration'])
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def get_file_size(file_path):
    """Get the file size in a human-readable format (KB, MB, etc.)."""
    size_bytes = os.path.getsize(file_path)
    size_kb = size_bytes / 1024  # Convert to KB
    if size_kb > 1024:
        size_mb = size_kb / 1024  # Convert to MB if larger than 1 MB
        return f"{size_mb:.2f} MB"
    else:
        return f"{size_kb:.2f} KB"

def get_audio_frequency(file_path):
    """Get the audio sample rate (frequency) in kHz."""
    try:
        info = mediainfo(file_path)
        sample_rate = int(info['sample_rate'])  # Sample rate is in Hz
        return f"{sample_rate / 1000} kHz"  # Convert to kHz
    except Exception as e:
        print(f"Error reading frequency from {file_path}: {e}")
        return None

def get_audio_channels(file_path):
    """Get the number of audio channels and return 'Mono' or 'Stereo'."""
    try:
        info = mediainfo(file_path)
        channels = int(info['channels'])
        if channels == 1:
            return "Mono"
        elif channels == 2:
            return "Stereo"
        else:
            return f"{channels} Channels"  # In case of more than 2 channels
    except Exception as e:
        print(f"Error reading channels from {file_path}: {e}")
        return None

def process_audio_files_in_folder(folder_path, output_excel):
    """Process all audio files in a folder and create an Excel with file names, durations, file sizes, frequencies, and channels."""
    # Create a new Excel workbook and active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Audio Files"
    ws.append(["File Name", "Duration (HH:MM:SS)", "File Size", "Frequency (kHz)", "Channels"])

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.wav', '.mp3', '.flac')):  # Add other formats if needed
            file_path = os.path.join(folder_path, file_name)
            duration = get_audio_duration(file_path)
            file_size = get_file_size(file_path)
            frequency = get_audio_frequency(file_path)
            channels = get_audio_channels(file_path)
            if duration is not None and frequency is not None and channels is not None:
                ws.append([file_name, duration, file_size, frequency, channels])

    # Save the Excel file
    wb.save(output_excel)
    print(f"Excel file created: {output_excel}")

# Example usage
folder_path = '/users/azizkhan/python/test_files/audio'  # Update with your actual folder path
output_excel = '/users/azizkhan/python/test_files/audio_durations.xlsx'  # Output Excel file path

process_audio_files_in_folder(folder_path, output_excel)
