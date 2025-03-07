import pandas as pd
import os

# Define file paths
base_path = "/Users/azizkhan/Desktop"  # Ensure correct path casing
file_1000 = os.path.join(base_path, "1000.csv")
file_1900 = os.path.join(base_path, "1900.csv")
podia_file = os.path.join(base_path, "podia.csv")
output_file = os.path.join(base_path, "updated_podia.csv")  # New output file

# Function to load CSV and rename columns
def load_csv(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        exit()

    df = pd.read_csv(file_path)
    
    # Rename columns to match podia.csv
    column_mapping = {
        "firstName": "first_name",
        "lastName": "last_name",
        "email": "email"
    }

    df = df.rename(columns=column_mapping)

    # Ensure all required columns exist
    required_columns = ["first_name", "last_name", "email"]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Missing required columns in {file_path}. Found columns: {df.columns.tolist()}")
        exit()

    return df[required_columns]

# Load and transform the source CSVs
df_1000 = load_csv(file_1000)
df_1900 = load_csv(file_1900)

# Combine the two source dataframes
df_combined = pd.concat([df_1000, df_1900], ignore_index=True)

# Save the new file
df_combined.to_csv(output_file, index=False)

print(f"Updated data saved to {output_file}")
