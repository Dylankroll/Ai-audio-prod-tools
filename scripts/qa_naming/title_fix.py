"""
title_fix.py

CSV or mapping-driven renaming helper for normalizing asset titles and
enforcing naming conventions.
"""

import os
import csv
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# Function to rename files based on the CSV mapping
def rename_files(target_folder, log_output):
    try:
        # Path to the CSV file in the script's root directory
        script_root = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_root, "Name Error Correction List - Sheet2.csv")

        # Check if CSV file exists
        if not os.path.exists(csv_file):
            log_output.insert(tk.END, f"Error: CSV file '{csv_file}' not found.\n")
            return

        # Load CSV file into a dictionary
        title_mapping = {}
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                correct_title = row['Correct Titles'].strip()
                present_title = row['Present Titles'].strip()
                title_mapping[present_title] = correct_title

        # Process each file in the target folder
        renamed_count = 0
        for filename in os.listdir(target_folder):
            file_path = os.path.join(target_folder, filename)

            # Check for valid audio files
            if not (filename.endswith(('.wav', '.mp3', '.flac')) and os.path.isfile(file_path)):
                continue  # Skip non-audio files or directories
            
            # Extract the prefix and title segment
            prefix, _, rest = filename.partition("_")
            if not rest:
                continue  # Skip files with unexpected formats
            
            title_segment = "_" + rest  # Reattach the underscore

            # Search for a match in the CSV title mapping
            for present_title, correct_title in title_mapping.items():
                if title_segment.startswith(present_title):
                    updated_title = title_segment.replace(present_title, correct_title, 1)
                    new_filename = f"{prefix}{updated_title}"
                    
                    # Handle path sanitization
                    new_path = os.path.join(target_folder, new_filename)
                    os.rename(file_path, new_path)
                    
                    # Log the change
                    log_output.insert(tk.END, f'Renamed: "{filename}" -> "{new_filename}"\n')
                    renamed_count += 1
                    break

        log_output.insert(tk.END, f"\nRenaming Complete: {renamed_count} files updated.\n")
        log_output.see(tk.END)  # Scroll to the end of the log

    except Exception as e:
        log_output.insert(tk.END, f"Error: {e}\n")

# Function to browse for folder
def browse_folder(entry_field):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, folder_selected)

# Function to start the renaming process
def start_renaming(folder_entry, log_output):
    target_folder = folder_entry.get().strip()

    # Validate folder path
    if not target_folder or not os.path.isdir(target_folder):
        messagebox.showerror("Error", "Please select a valid folder containing audio files.")
        return

    log_output.delete(1.0, tk.END)  # Clear previous logs
    log_output.insert(tk.END, f"Processing folder: {target_folder}\n\n")
    rename_files(target_folder, log_output)

# Build the Tkinter GUI
def build_gui():
    # Root window
    root = tk.Tk()
    root.title("Audio File Renamer")
    root.geometry("700x500")
    root.resizable(False, False)

    # Instructions Label
    tk.Label(root, text="Select the folder containing your audio files:", font=("Arial", 12)).pack(pady=10)

    # Folder Input Frame
    folder_frame = tk.Frame(root)
    folder_frame.pack(pady=5)

    folder_entry = tk.Entry(folder_frame, width=60, font=("Arial", 10))
    folder_entry.pack(side=tk.LEFT, padx=(0, 5))

    browse_button = tk.Button(folder_frame, text="Browse", command=lambda: browse_folder(folder_entry))
    browse_button.pack(side=tk.RIGHT)

    # Run Button
    run_button = tk.Button(root, text="Run Script", font=("Arial", 12), bg="green", fg="white",
                           command=lambda: start_renaming(folder_entry, log_output))
    run_button.pack(pady=15)

    # Log Output Area
    tk.Label(root, text="Output Log:", font=("Arial", 12)).pack()
    log_output = scrolledtext.ScrolledText(root, width=80, height=20, font=("Arial", 10))
    log_output.pack(pady=10)

    # Start the GUI
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    build_gui()
