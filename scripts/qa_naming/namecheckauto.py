"""
namecheckauto.py

Naming and inventory checker. Compares expected outputs (from mapping files)
against actual files on disk to catch missing or misnamed assets early.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from itertools import combinations

def select_root_folder():
    folder_path = filedialog.askdirectory(title="Select Root Folder to Analyze")
    root_folder_var.set(folder_path)

def load_reference_files(mapping_types):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mapping_dir = os.path.join(script_dir, "mappings")

    if not os.path.exists(mapping_dir):
        messagebox.showerror("Error", f"Mapping directory '{mapping_dir}' not found!")
        return None

    reference_files = []
    if "Names" in mapping_types:
        reference_files.extend([
            "1-SYL.txt", "2-SYL_001.txt", "2-SYL_002.txt",
            "2-SYL_003.txt", "2-SYL_004.txt", "3-SYL.txt", "4-SYL.txt"
        ])
    if "Ordinal (Numbers)" in mapping_types:
        reference_files.extend([f"{i}_NUM_ORD.txt" for i in range(1, 5)])
    if "Cardinal (Numbers)" in mapping_types:
        reference_files.extend([f"{i}_NUM_CAR.txt" for i in range(1, 5)])

    references = {}
    for file_name in reference_files:
        file_path = os.path.join(mapping_dir, file_name)
        if os.path.exists(file_path):
            ref_key = file_name.split(".")[0]
            if "NUM" in ref_key:
                ref_key = f"{ref_key.split('_')[0]}-SYL_NUM"
            with open(file_path, "r") as f:
                references.setdefault(ref_key, []).extend(
                    line.strip() for line in f if line.strip() and "REMOVE" not in line
                )
        else:
            messagebox.showerror("Error", f"Reference file {file_name} not found!")
            return None
    return references

def analyze_files():
    root_folder = root_folder_var.get().strip().strip('"')  # Sanitize the path
    mapping_types = [var.get() for var in mapping_type_vars if var.get()]
    mode = analysis_mode_var.get()

    if not root_folder:
        messagebox.showerror("Error", "Please select a root folder to analyze.")
        return

    references = load_reference_files(mapping_types)
    if not references:
        return

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    if mode == "Root Folder":
        try:
            actual_files = {
                os.path.splitext(file[file.find('_'):])[0]
                for file in os.listdir(root_folder)
                if os.path.isfile(os.path.join(root_folder, file)) and '_' in file
            }
        except Exception as e:
            messagebox.showerror("Error", f"Could not read the root folder: {e}")
            return

        for ref_name, expected_files in references.items():
            reference_set = {os.path.splitext(name)[0] for name in expected_files}
            missing_files = reference_set - actual_files

            result_text.insert(tk.END, f"Analysis for reference: {ref_name}\n")
            if missing_files:
                result_text.insert(tk.END, "  Missing files:\n")
                for file in sorted(missing_files):
                    result_text.insert(tk.END, f"    {file}\n")
            else:
                result_text.insert(tk.END, "  All files listed are present.\n")
            result_text.insert(tk.END, "\n")

    elif mode == "Subfolders":
        try:
            subfolders = {folder.strip(): folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))}
        except Exception as e:
            messagebox.showerror("Error", f"Could not read the root folder: {e}")
            return

        for folder_key, expected_files in references.items():
            if folder_key.endswith("-SYL_NUM"):
                num_key = folder_key
            else:
                num_key = folder_key

            subfolder_path = subfolders.get(num_key)

            if not subfolder_path:
                result_text.insert(tk.END, f"Missing subfolder for: {num_key}\n")
                continue

            full_subfolder_path = os.path.join(root_folder, subfolder_path)
            try:
                actual_files = {
                    os.path.splitext(file[file.find('_'):])[0]
                    for file in os.listdir(full_subfolder_path)
                    if '_' in file
                }
            except Exception as e:
                result_text.insert(tk.END, f"Error reading subfolder {folder_key}: {e}\n")
                continue

            reference_set = {os.path.splitext(name)[0] for name in expected_files}
            missing_files = reference_set - actual_files

            result_text.insert(tk.END, f"Analysis for subfolder: {num_key}\n")
            if missing_files:
                result_text.insert(tk.END, "  Missing files:\n")
                for file in sorted(missing_files):
                    result_text.insert(tk.END, f"    {file}\n")
            else:
                result_text.insert(tk.END, "  All files listed are present.\n")
            result_text.insert(tk.END, "\n")

    result_text.config(state=tk.DISABLED)

def auto_analyze():
    root_folder = root_folder_var.get().strip().strip('"')  # Sanitize the path

    if not root_folder:
        messagebox.showerror("Error", "Please select a root folder to analyze.")
        return

    is_single_folder = True
    try:
        items = os.listdir(root_folder)
        for item in items:
            if os.path.isdir(os.path.join(root_folder, item)):
                is_single_folder = False
                break
    except Exception as e:
        messagebox.showerror("Error", f"Could not read the root folder: {e}")
        return

    best_mapping = None
    max_matches = 0
    min_missing_files = float('inf')

    print("Starting analysis...")

    # Combinations excluding "Ordinal (Numbers)" and "Cardinal (Numbers)" together
    possible_combinations = [
        ("Names",),
        ("Ordinal (Numbers)",),
        ("Cardinal (Numbers)",),
        ("Names", "Ordinal (Numbers)"),
        ("Names", "Cardinal (Numbers)"),
    ]

    for mapping_comb in possible_combinations:
        print(f"Trying combination: {mapping_comb}")
        references = load_reference_files(mapping_comb)
        if not references:
            print("No references found for this combination.")
            continue

        match_count = 0
        total_missing_files = 0
        valid_combination = False

        if is_single_folder:
            try:
                actual_files = {
                    os.path.splitext(file[file.find('_'):])[0]
                    for file in os.listdir(root_folder)
                    if os.path.isfile(os.path.join(root_folder, file)) and '_' in file
                }
            except Exception as e:
                messagebox.showerror("Error", f"Could not read the root folder: {e}")
                return

            for expected_files in references.values():
                reference_set = {os.path.splitext(name)[0] for name in expected_files}
                matches = reference_set & actual_files
                match_count += len(matches)
                missing_files = reference_set - actual_files
                total_missing_files += len(missing_files)
                print(f"Matches for combination {mapping_comb}: {match_count}, Missing files: {len(missing_files)}")
                if match_count > 0:
                    valid_combination = True

        else:
            try:
                subfolders = {folder.strip(): folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))}
            except Exception as e:
                messagebox.showerror("Error", f"Could not read the root folder: {e}")
                return

            for folder_key, expected_files in references.items():
                if folder_key.endswith("-SYL_NUM"):
                    num_key = folder_key
                else:
                    num_key = folder_key

                subfolder_path = subfolders.get(num_key)
                if not subfolder_path:
                    total_missing_files += len(expected_files)
                    continue

                full_subfolder_path = os.path.join(root_folder, subfolder_path)
                try:
                    actual_files = {
                        os.path.splitext(file[file.find('_'):])[0]
                        for file in os.listdir(full_subfolder_path)
                        if '_' in file
                    }
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading subfolder {folder_key}: {e}\n")
                    continue

                reference_set = {os.path.splitext(name)[0] for name in expected_files}
                matches = reference_set & actual_files
                match_count += len(matches)
                missing_files = reference_set - actual_files
                total_missing_files += len(missing_files)
                print(f"Matches for combination {mapping_comb}: {match_count}, Missing files: {len(missing_files)}")
                if match_count > 0:
                    valid_combination = True

        if valid_combination and (match_count > max_matches or (match_count == max_matches and total_missing_files < min_missing_files)):
            max_matches = match_count
            min_missing_files = total_missing_files
            best_mapping = mapping_comb

    if best_mapping:
        print(f"Best mapping found: {best_mapping} with {max_matches} matches and {min_missing_files} missing files")
        # Set the mapping_type_vars based on the best_mapping
        for var, text in zip(mapping_type_vars, ["Names", "Ordinal (Numbers)", "Cardinal (Numbers)"]):
            if text in best_mapping:
                var.set(text)
            else:
                var.set("")
        # Set the analysis mode
        if is_single_folder:
            analysis_mode_var.set("Root Folder")
        else:
            analysis_mode_var.set("Subfolders")
        # Run the analysis with the best mapping
        print(f"Running analysis with mapping: {best_mapping}")
        analyze_files()
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No suitable mapping type found.\n")
        result_text.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Title Checker")
root.geometry("800x700")

root_folder_var = tk.StringVar()
mapping_type_vars = [tk.StringVar() for _ in range(3)]
analysis_mode_var = tk.StringVar(value="Subfolders")  # Default to "Subfolders"

tk.Label(root, text="Root Folder to Analyze:").pack(pady=5)
tk.Entry(root, textvariable=root_folder_var, width=60).pack()
tk.Button(root, text="Browse Root Folder", command=select_root_folder).pack(pady=5)

tk.Label(root, text="Mapping Type:").pack(pady=5)

mapping_frame = tk.Frame(root)
mapping_frame.pack(pady=5)
for text, var in zip(["Names", "Ordinal (Numbers)", "Cardinal (Numbers)"], mapping_type_vars):
    tk.Checkbutton(mapping_frame, text=text, variable=var, onvalue=text, offvalue="").pack(side=tk.LEFT)

mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)
tk.Label(root, text="Analysis Mode:").pack(pady=5)
tk.Radiobutton(mode_frame, text="Subfolders", variable=analysis_mode_var, value="Subfolders").pack(side=tk.LEFT)
tk.Radiobutton(mode_frame, text="Single Folder", variable=analysis_mode_var, value="Root Folder").pack(side=tk.LEFT)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Analyze Files", command=analyze_files, bg="yellow", fg="black").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Auto-Analyze", command=auto_analyze, bg="orange", fg="black").pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Results:").pack(pady=5)
result_text = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED)
result_text.pack(pady=5)

root.mainloop()
