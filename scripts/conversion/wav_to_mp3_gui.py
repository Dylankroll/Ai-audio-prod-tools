"""
wav_to_mp3_gui.py

Batch conversion helper for preparing delivery formats (WAV to MP3). Uses FFmpeg
through pydub and is intended for local-file workflows.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pydub import AudioSegment
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffprobe   = "/opt/homebrew/bin/ffprobe"

def log_message(msg):
    log_area.insert(tk.END, msg + "\n")
    log_area.see(tk.END)  # Auto-scroll to the bottom

def convert_wavs_to_mp3(folder_path):
    folder_path = os.path.expanduser(folder_path.strip())
    if not os.path.isdir(folder_path):
        messagebox.showerror("Invalid Path", f"Folder not found:\n{folder_path}")
        return

    converted_folder = os.path.join(folder_path, "converted")
    os.makedirs(converted_folder, exist_ok=True)

    wav_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".wav")]

    if not wav_files:
        messagebox.showinfo("No Files", "No WAV files found in the selected folder.")
        return

    log_area.delete(1.0, tk.END)
    log_message(f"Found {len(wav_files)} WAV files.")
    log_message(f"Converting to: {converted_folder}")

    for wav_file in wav_files:
        wav_path = os.path.join(folder_path, wav_file)
        mp3_name = os.path.splitext(wav_file)[0] + ".mp3"
        mp3_path = os.path.join(converted_folder, mp3_name)

        try:
            audio = AudioSegment.from_wav(wav_path)
            audio.export(mp3_path, format="mp3", bitrate="192k")
            log_message(f"✓ Converted: {wav_file}")
        except Exception as e:
            log_message(f"✗ Failed: {wav_file} — {e}")

    log_message("✅ Conversion complete.")

def browse_folder():
    selected = filedialog.askdirectory()
    if selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, selected)

def on_convert_click():
    folder = folder_entry.get()
    convert_wavs_to_mp3(folder)

# GUI Setup
root = tk.Tk()
root.title("WAV to MP3 Batch Converter")

tk.Label(root, text="Select Folder with WAV Files:").pack(pady=(10, 0))

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=5, fill=tk.X)

folder_entry = tk.Entry(entry_frame, width=50)
folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

browse_button = tk.Button(entry_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.RIGHT, padx=(5, 0))

convert_button = tk.Button(root, text="Convert to MP3", command=on_convert_click)
convert_button.pack(pady=10)

# Log/Output area
log_area = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
log_area.pack(padx=10, pady=(0, 10))

root.mainloop()