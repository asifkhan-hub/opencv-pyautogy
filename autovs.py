import subprocess
import pyautogui
import time

# Function to open LibreOffice Writer
def open_libreoffice():
    subprocess.Popen(["libreoffice", "--writer"])
    time.sleep(5)  # Wait for LibreOffice to open (adjust delay as needed)

# Function to create or edit a document
def create_or_edit_document(document_name):
    # Simulate pressing Ctrl+N to create a new document or open an existing one
    pyautogui.hotkey("ctrl", "n")
    time.sleep(1)  # Wait for the document to open (adjust delay as needed)

    # Type the document name and press Enter (modify as needed)
    pyautogui.write(document_name)
    pyautogui.press("enter")
    time.sleep(1)  # Wait for the document to load (adjust delay as needed)

# Function to type text into the document
def type_text(text):
    pyautogui.write(text)

# Function to save the document
def save_document(file_name):
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)  # Wait for the Save dialog to open (adjust delay as needed)

    # Type the file name and press Enter (modify as needed)
    pyautogui.write(file_name)
    pyautogui.press("enter")
    time.sleep(1)  # Wait for the document to be saved (adjust delay as needed)

# Function to print the document
def print_document():
    pyautogui.hotkey("ctrl", "p")
    time.sleep(1)  # Wait for the Print dialog to open (adjust delay as needed)

    # Send Enter to print the document with default settings
    pyautogui.press("enter")
    time.sleep(1)  # Wait for the document to be printed (adjust delay as needed)

# Main script
if __name__ == "__main__":
    # Open LibreOffice Writer
    open_libreoffice()

    # Create or edit a document named "example.odt"
    create_or_edit_document("example.odt")

    # Type some text into the document
    type_text("This is an automated LibreOffice document.")

    # Save the document as "my_document.odt"
    save_document("my_document.odt")

    # Print the document
    print_document()
