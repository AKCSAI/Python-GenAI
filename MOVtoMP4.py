import os
import subprocess

def convert_all_mov_to_mp4(source_folder):
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"The source folder {source_folder} does not exist.")
        return

    # Extract the name of the source folder and create an output folder name
    source_folder_name = os.path.basename(os.path.normpath(source_folder))
    output_folder_name = f"{source_folder_name}_output"
    output_folder = os.path.join(os.path.dirname(source_folder), output_folder_name)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Output folder created: {output_folder}")
    else:
        print(f"Output folder already exists: {output_folder}")
    
    # Iterate through all the files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".mov"):
            input_file = os.path.join(source_folder, filename)
            # Generate the output file path in the output folder, changing the extension to .mp4
            output_file = os.path.join(output_folder, filename.replace(".mov", ".mp4"))
            
            # Construct the ffmpeg command
            command = ['ffmpeg', '-i', input_file, output_file]
            
            # Execute the ffmpeg command
            try:
                print(f"Converting {input_file} to {output_file}")
                subprocess.run(command, check=True)
                print(f"Successfully converted {filename} to .mp4")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while converting {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

# Example usage
source_folder = 'path/to/your/source_folder'  # Replace with the path to your folder containing .mov files

convert_all_mov_to_mp4(source_folder)
