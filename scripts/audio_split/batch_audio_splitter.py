"""
batch_audio_splitter.py

Batch audio splitting tool driven by mapping files. Built for repeatable
segmentation and naming of narration or voice assets in production workflows.
"""

import subprocess
import math
import re
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

# Determine the base directory (whether running from source or from the packaged app)
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS  # Temporary directory where PyInstaller unpacks the app
else:
    base_dir = os.path.dirname(__file__)

# Default folder (can be updated by user input)
default_folder = base_dir

# File mappings (updated dynamically based on the selected folder)
def get_file_mappings(selected_folder):
    mappings_dir = os.path.join(base_dir, 'mappings')  # Always reference 'mappings' from script directory
    return {
        '1-SYL.wav': os.path.join(selected_folder, '1-SYL.wav'),
        '2-SYL_001.wav': os.path.join(selected_folder, '2-SYL_001.wav'),
        '2-SYL_002.wav': os.path.join(selected_folder, '2-SYL_002.wav'),
        '2-SYL_003.wav': os.path.join(selected_folder, '2-SYL_003.wav'),
        '2-SYL_004.wav': os.path.join(selected_folder, '2-SYL_004.wav'),
        '3-SYL.wav': os.path.join(selected_folder, '3-SYL.wav'),
        '4-SYL.wav': os.path.join(selected_folder, '4-SYL.wav'),
    }, {
        '1-SYL.wav': os.path.join(mappings_dir, '1-SYL.txt'),
        '2-SYL_001.wav': os.path.join(mappings_dir, '2-SYL_001.txt'),
        '2-SYL_002.wav': os.path.join(mappings_dir, '2-SYL_002.txt'),
        '2-SYL_003.wav': os.path.join(mappings_dir, '2-SYL_003.txt'),
        '2-SYL_004.wav': os.path.join(mappings_dir, '2-SYL_004.txt'),
        '3-SYL.wav': os.path.join(mappings_dir, '3-SYL.txt'),
        '4-SYL.wav': os.path.join(mappings_dir, '4-SYL.txt'),
    }

# Function to sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '_', name)

# Function to get the total duration of the audio file using ffprobe
def get_audio_duration(filename):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

# Function to split a single audio file into clips
def split_audio_file(audio_file, titles_file, clip_duration, title_prefix, output_folder):
    with open(titles_file, 'r', encoding='utf-8') as f:
        titles = [line.strip() for line in f if line.strip()]
    try:
        total_duration = get_audio_duration(audio_file)
    except Exception as e:
        print(f"Error retrieving audio duration for {audio_file}: {e}")
        return
    num_clips = math.ceil(total_duration / clip_duration)
    if num_clips > len(titles):
        print(f"Error: Not enough titles for the number of clips in {audio_file} ({num_clips} required).")
        return
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    output_dir = os.path.join(output_folder, base_name)
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_clips):
        start_time = i * clip_duration
        duration = min(clip_duration, total_duration - start_time)
        sanitized_title = sanitize_filename(f"{title_prefix}{titles[i]}")
        output_file = os.path.join(output_dir, f"{sanitized_title}.wav")
        command = [
            'ffmpeg',
            '-y',
            '-i', audio_file,
            '-ss', str(start_time),
            '-t', str(duration),
            output_file
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"Created clip: {output_file}")

# Function to delete files with "REMOVE" in their filename
def cleanup_remove_files(file_mappings, output_folder):
    for audio_file in file_mappings.keys():
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_dir = os.path.join(output_folder, base_name)
        if os.path.isdir(output_dir):
            for filename in os.listdir(output_dir):
                if "REMOVE" in filename.upper():
                    file_path = os.path.join(output_dir, filename)
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except OSError as e:
                        print(f"Error deleting file {file_path}: {e}")

# Function to start processing with GUI inputs
def start_processing():
    try:
        clip_duration = float(duration_entry.get())
        title_prefix = prefix_entry.get()
        selected_folder = folder_entry.get()
        sanitized_folder = os.path.normpath(selected_folder)
        audio_file_mappings, title_file_mappings = get_file_mappings(sanitized_folder)
        output_folder = sanitized_folder

        for audio_file, titles_file in audio_file_mappings.items():
            titles_file_path = title_file_mappings.get(audio_file)
            if not os.path.isfile(audio_file):
                print(f"Missing audio file: {audio_file}")
                continue
            if not os.path.isfile(titles_file_path):
                print(f"Missing title file: {titles_file_path}")
                continue
            print(f"Processing {audio_file} with titles from {titles_file_path}...")
            split_audio_file(audio_file, titles_file_path, clip_duration, title_prefix, output_folder)

        cleanup_remove_files(audio_file_mappings, output_folder)

        print("All audio files have been processed successfully.")
        messagebox.showinfo("Success", "All audio files have been processed successfully.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for clip duration.")

# Function to browse for a folder
def browse_folder():
    folder_selected = filedialog.askdirectory(title="Select Folder")
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

# Create the main window
root = tk.Tk()
root.title("Batch Audio Splitter")

# Folder selection
folder_frame = tk.LabelFrame(root, text="Target Folder")
folder_frame.pack(pady=10, padx=10, fill="x")
folder_entry = tk.Entry(folder_frame, width=50)
folder_entry.insert(0, default_folder)
folder_entry.pack(side="left", padx=5, pady=5)
browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side="left", padx=5)

# Clip duration entry
duration_label = tk.Label(root, text="Clip Duration (seconds):")
duration_label.pack(pady=5)
duration_entry = tk.Entry(root)
duration_entry.insert(0, "2")
duration_entry.pack(pady=5)

# Title prefix entry
prefix_label = tk.Label(root, text="Title Prefix:")
prefix_label.pack(pady=5)
prefix_entry = tk.Entry(root)
prefix_entry.insert(0, "1.1.1.1")
prefix_entry.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start Processing", command=start_processing)
start_button.pack(pady=20)

# Run the application
root.mainloop()
