import csv
import os
import re

def format_time_in_csv(csv_file_path):
    """Format the Time column in the CSV file to MM:SS if hours are zero."""
    updated_data = []
    
    # Read the existing CSV and update the time format
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Keep the header

        # Process each row
        for row in csv_reader:
            time_str = row[1]  # Assuming 'Time' is the second column
            parts = time_str.split(":")
            
            # If the time is in HH:MM:SS format and hours are zero, convert to MM:SS
            if len(parts) == 3 and parts[0] == '00':
                row[1] = f"{parts[1]}:{parts[2]}"  # Convert to MM:SS
            updated_data.append(row)
    
    # Write the updated data back to the CSV
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)  # Write header
        csv_writer.writerows(updated_data)  # Write updated rows

def convert_txt_to_csv(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Regex patterns to identify speaker, time lines, and embedded timestamps
    speaker_time_pattern = re.compile(r'(Speaker \d+)\s+\((\d{2}:\d{2})\):')
    embedded_time_pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]')

    # Loop through all .txt files in the input directory
    for txt_file_name in os.listdir(input_dir):
        if txt_file_name.endswith('.txt'):
            txt_file_path = os.path.join(input_dir, txt_file_name)
            csv_file_path = os.path.join(output_dir, os.path.splitext(txt_file_name)[0] + '.csv')

            try:
                # Read the text file and structure data
                structured_data = []
                current_person = None
                current_time = None
                current_text = []

                with open(txt_file_path, 'r') as txt_file:
                    for line in txt_file:
                        # Check if the line matches the speaker and time format
                        match = speaker_time_pattern.match(line.strip())
                        if match:
                            # If we have already captured some text, store it before starting the next entry
                            if current_person and current_time and current_text:
                                structured_data.append([current_person, current_time, " ".join(current_text).strip()])
                            
                            # Update speaker and time, reset text
                            current_person = match.group(1)
                            current_time = match.group(2)
                            current_text = []
                        else:
                            # Check for embedded timestamps in the text
                            embedded_matches = embedded_time_pattern.findall(line)
                            if embedded_matches:
                                # Split the text on the embedded timestamps and handle each segment
                                segments = embedded_time_pattern.split(line.strip())
                                for i, segment in enumerate(segments):
                                    if i % 2 == 1:  # Odd indices are timestamps
                                        # Save the current text before the timestamp
                                        if current_text:
                                            structured_data.append([current_person, current_time, " ".join(current_text).strip()])
                                            current_text = []
                                        # Now start a new row with the embedded timestamp
                                        current_time = segment.strip()
                                    else:
                                        # Add the following text after the timestamp
                                        if segment.strip():
                                            current_text.append(segment.strip())
                            else:
                                # Add normal text lines to the current dialogue
                                current_text.append(line.strip())

                    # Add the last entry if it exists
                    if current_person and current_time and current_text:
                        structured_data.append([current_person, current_time, " ".join(current_text).strip()])

                # Write to the CSV file with specified columns
                with open(csv_file_path, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(["Person", "Time", "Text"])  # Write header
                    csv_writer.writerows(structured_data)  # Write data rows

                # Post-process the CSV to format the time column
                format_time_in_csv(csv_file_path)

                print(f"Converted {txt_file_name} to CSV and formatted time successfully!")
            except Exception as e:
                print(f"An error occurred with {txt_file_name}: {e}")

# Run the conversion
input_dir = '/users/azizkhan/python/test_files/'  # Replace with your actual input directory
output_dir = '/users/azizkhan/python/test_files/output_files/'  # Replace with your desired output directory
convert_txt_to_csv(input_dir, output_dir)