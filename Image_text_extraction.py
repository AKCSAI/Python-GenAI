from PIL import Image
import pytesseract

# Function to extract text from an image
def extract_text_from_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)

        # Return the extracted text
        return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Define the image path in the program itself
    image_path = "/Users/AzizKhan/Desktop/image1.png"  # Replace with your actual image path

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)
