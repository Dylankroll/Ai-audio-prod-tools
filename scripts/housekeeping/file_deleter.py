"""
file_deleter.py

Controlled cleanup utility driven by explicit mapping rules. Intended for
removing known-unwanted files in bulk. Review mappings carefully before running.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

class AudioFileDeleterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio File Deleter")

        # Store the selected directory path
        self.selected_directory = tk.StringVar()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Label + Entry to show selected folder
        tk.Label(self.master, text="Selected Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.master, textvariable=self.selected_directory, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Browse Button
        browse_button = tk.Button(self.master, text="Browse...", command=self.browse_folder)
        browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Delete Button
        delete_button = tk.Button(self.master, text="Delete Files", command=self.delete_files)
        delete_button.grid(row=1, column=1, pady=10, sticky="n")

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_directory.set(folder_path)

    def delete_files(self):
        # 1. Get the raw folder path from our StringVar
        raw_path = self.selected_directory.get().strip()
        if not raw_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return

        # 2. Sanitize the path to remove surrounding quotes and normalize
        sanitized_path = raw_path.strip('"')  # remove extraneous quotes
        folder_path = os.path.normpath(sanitized_path)  # normalize path

        # Check that the directory actually exists
        if not os.path.isdir(folder_path):
            messagebox.showerror("Invalid Folder", f"The folder '{folder_path}' does not exist or is invalid.")
            return

        # 3. Build path to custom_map.txt
        script_dir = os.path.dirname(os.path.abspath(__file__))
        map_file_path = os.path.join(script_dir, "mappings", "custom_map.txt")

        if not os.path.exists(map_file_path):
            messagebox.showerror("File Not Found", f"The file {map_file_path} does not exist.")
            return

        # 4. Read lines from custom_map.txt
        with open(map_file_path, "r", encoding="utf-8") as f:
            patterns = [line.strip() for line in f if line.strip()]

        if not patterns:
            messagebox.showinfo("No Patterns", "No patterns found in custom_map.txt.")
            return

        # 5. Count of deleted files
        deleted_count = 0

        # 6. Iterate through files in the selected folder
        for filename in os.listdir(folder_path):
            # Optional: check common audio extensions
            if filename.lower().endswith((".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a")):
                file_path = os.path.join(folder_path, filename)

                # Check if any of the patterns is a substring in the filename
                for pattern in patterns:
                    if pattern in filename:
                        try:
                            os.remove(file_path)
                            deleted_count += 1
                            print(f"Deleted file: {filename}")
                        except Exception as e:
                            print(f"Error deleting file '{filename}': {e}")
                        break  # Stop checking other patterns once deleted

        messagebox.showinfo("Deletion Complete", f"Deleted {deleted_count} files.")

def main():
    root = tk.Tk()
    app = AudioFileDeleterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
