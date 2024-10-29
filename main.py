import streamlit as st
import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime


# Step 1: Function to create folders based on file extensions
def organize_files_by_extension(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extension_map = {
        'images': ['.jpg', '.jpeg', '.png', '.gif'],
        'videos': ['.mp4', '.avi', '.mov'],
        'documents': ['.pdf', '.docx', '.txt'],
        # Add other extensions as needed
    }

    # Step 2: Organize files
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = Path(file).suffix.lower()
            category = 'others'  # Default folder

            for folder, extensions in extension_map.items():
                if file_extension in extensions:
                    category = folder
                    break

            # Create directory and move file
            target_folder = os.path.join(output_folder, category)
            os.makedirs(target_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(target_folder, file))


# Streamlit UI
st.title("Folder Organizer by File Type")
st.write("Upload a zip file of your folder, and the app will organize files into folders based on file types.")

uploaded_file = st.file_uploader("Upload Folder (Zip file)", type="zip")
if uploaded_file:
    # Step 3: Extract and organize
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("uploaded_folder")

    # Add timestamp to output directory name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"organized_folder_{timestamp}"
    organize_files_by_extension("uploaded_folder", output_dir)

    # Rezip the organized folder for download
    shutil.make_archive(output_dir, 'zip', output_dir)
    with open(f"{output_dir}.zip", "rb") as file:
        st.download_button("Download Organized Folder", file, f"{output_dir}.zip")

    # Cleanup extracted and organized folders
    shutil.rmtree("uploaded_folder")
    shutil.rmtree(output_dir)
