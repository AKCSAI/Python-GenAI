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

def process_audio_files_in_folder(folder_path, output_excel):
    """Process all audio files in a folder and create an Excel with file names and durations."""
    # Create a new Excel workbook and active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Audio Files"
    ws.append(["File Name", "Duration (HH:MM:SS)"])

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.wav', '.mp3', '.flac')):  # Add other formats if needed
            file_path = os.path.join(folder_path, file_name)
            duration = get_audio_duration(file_path)
            if duration is not None:
                ws.append([file_name, duration])

    # Save the Excel file
    wb.save(output_excel)
    print(f"Excel file created: {output_excel}")

# Example usage
folder_path = '/users/azizkhan/python/test_files/audio'  # Update with your actual folder path
output_excel = '/users/azizkhan/python/test_files/audio_durations.xlsx'  # Output Excel file path

process_audio_files_in_folder(folder_path, output_excel)

