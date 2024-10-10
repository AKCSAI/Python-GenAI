from pydub import AudioSegment
import os

def convert_mp3_to_wav(input_folder, output_folder):
    try:
        # Iterate through all subfolders and files in the input folder
        for root, _, files in os.walk(input_folder):
            # Create a corresponding output subfolder
            relative_path = os.path.relpath(root, input_folder)
            current_output_folder = os.path.join(output_folder, relative_path)
            os.makedirs(current_output_folder, exist_ok=True)
            
            for file in files:
                if file.endswith(".mp3"):
                    input_file_path = os.path.join(root, file)
                    output_file_name = os.path.splitext(file)[0] + ".wav"
                    output_file_path = os.path.join(current_output_folder, output_file_name)
                    
                    # Load the mp3 file
                    audio = AudioSegment.from_mp3(input_file_path)
                    
                    # Export the audio in WAV format
                    audio.export(output_file_path, format="wav")
                    print(f"Successfully converted {input_file_path} to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_folder = "input_folder_path"  # Path to the input folder containing MP3 files
output_folder = "output_folder_path"  # Path to the output folder

# Convert MP3 to WAV
convert_mp3_to_wav(input_folder, output_folder)