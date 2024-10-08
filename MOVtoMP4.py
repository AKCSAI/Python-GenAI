import os
import subprocess

def convert_mov_to_mp4(input_file, output_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    # Construct the ffmpeg command
    command = ['ffmpeg', '-i', input_file, output_file]

    # Execute the ffmpeg command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
input_file = 'FilePathHere'  # Replace with your input file path
output_file = 'FilePathHere'  # Replace with your desired output file path

convert_mov_to_mp4(input_file, output_file)
