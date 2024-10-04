import boto3
import os
import re
from pydub import AudioSegment

# Get credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Set up Amazon Polly client with AWS credentials
polly = boto3.client('polly', region_name='us-west-2',
                     aws_access_key_id=aws_access_key_id,
                     aws_secret_access_key=aws_secret_access_key)

# List of available voices for Amazon Polly (you can add or change voices as needed)
available_voices = [
    'Joanna', 'Matthew', 'Amy', 'Brian', 'Emma', 'Ivy', 'Kendra', 'Kimberly', 'Salli', 'Joey', 'Justin', 'Nicole', 'Russell'
]

# Function to generate audio using Amazon Polly
def generate_audio(text, output_folder, filename, voice_id):
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id
        )
        
        # Save the output to a file
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'wb') as file:
            file.write(response['AudioStream'].read())
            print(f"Generated audio saved to {output_path}")

        # Generate a faster version of the audio
        audio = AudioSegment.from_mp3(output_path)
        faster_audio = audio.speedup(playback_speed=1.25)
        faster_output_path = os.path.join(output_folder, f"faster_{filename}")
        faster_audio.export(faster_output_path, format="mp3")
        print(f"Generated faster audio saved to {faster_output_path}")

        # Generate a faster version of the audio (1.5x speed)
        faster_audio_1_5X = audio.speedup(playback_speed=1.5)
        faster_output_path_1_5X = os.path.join(output_folder, f"faster_1_5X_{filename}")
        faster_audio_1_5X.export(faster_output_path_1_5X, format="mp3")
        print(f"Generated 1.5x faster audio saved to {faster_output_path_1_5X}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to clean the command and create a valid filename
def sanitize_filename(text):
    sanitized = re.sub(r'[<>:"/\\|?*]', '', text).replace(' ', '_')
    return sanitized

# Create folders for each voice
def create_folders(base_folder):
    for voice in available_voices:
        voice_folder = os.path.join(base_folder, voice)
        os.makedirs(voice_folder, exist_ok=True)
    print(f"Created folders for voices: {', '.join(available_voices)}.")

# Load commands from CSV file
def load_commands(csv_file):
    with open(csv_file, 'r') as file:
        commands = [line.strip() for line in file]
    return commands

# Generate speech commands for each voice
def generate_speech_commands(csv_file, base_output_folder):
    # Load commands from CSV file
    commands = load_commands(csv_file)

    # Create folders for each voice
    create_folders(base_output_folder)

    # Generate audio for each voice and command
    for voice_id in available_voices:
        voice_folder = os.path.join(base_output_folder, voice_id)

        for command in commands:
            # Sanitize the command and use it as the filename
            filename = f"{sanitize_filename(command)}.mp3"
            generate_audio(command, voice_folder, filename, voice_id)

    print(f"Audio generation completed for {len(available_voices)} voices.")

# Example usage with your CSV file path
csv_file_path = "/users/azizkhan/GitVersions/AI/commands.csv"  # Path to your CSV file
base_output_folder = "generated_voices"

# Run the function to generate speech commands
generate_speech_commands(csv_file_path, base_output_folder)


