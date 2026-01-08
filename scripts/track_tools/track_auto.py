"""
track_auto.py

Utility for organizing AI-generated narration outputs into track-based timelines
for post-production. Designed for script or slide-based narration workflows.
"""

import pyautogui
import time
import os
import tkinter as tk
from tkinter import messagebox

# Load slide numbers
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(script_dir, "slide_numbers.txt")
with open(txt_path, "r") as f:
    slide_numbers = [line.strip() for line in f if line.strip()]

def create_tracks():
    track_button.config(state="disabled", bg="yellow")
    root.update()
    print("Track creation starts in 5 seconds...")
    time.sleep(5)
    pyautogui.keyDown("command")
    for _ in range(len(slide_numbers) - 1):
        pyautogui.press("d")
        time.sleep(0.1)
    pyautogui.keyUp("command")
    messagebox.showinfo("Tracks Created", "Track creation complete.")
    track_button.config(state="normal", bg=default_bg)

def start_typing():
    slide_button.config(state="disabled", bg="yellow")
    root.update()
    print("Slide typing starts in 5 seconds...")
    time.sleep(5)
    for slide in slide_numbers:
        pyautogui.typewrite(slide)
        pyautogui.press("tab")
    messagebox.showinfo("Done", "All slide numbers have been typed.")
    slide_button.config(state="normal", bg=default_bg)

# GUI Setup
root = tk.Tk()
root.title("Slide Number Typer")
root.geometry("380x160")

default_bg = root.cget("bg")

label = tk.Label(root, text=f"{len(slide_numbers)} tracks detected.")
label.pack(pady=10)

track_button = tk.Button(root, text="Create Tracks", command=create_tracks)
track_button.pack(pady=5)

slide_button = tk.Button(root, text="Start Typing Slides", command=start_typing)
slide_button.pack(pady=5)

root.mainloop()