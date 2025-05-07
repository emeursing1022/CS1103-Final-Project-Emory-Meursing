# -*- coding: utf-8 -*-
"""
@author: Emory Meursing
"""

import requests
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import io
import os
import platform
import subprocess

session_images = []

def get_cat_photos_dir():
    desktop = Path.home() / "Desktop"
    cat_photos_dir = desktop / "cat photos"
    cat_photos_dir.mkdir(exist_ok=True)
    return cat_photos_dir

def fetch_and_save_cat_image(message=None):
    cat_photos_dir = get_cat_photos_dir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cat_{timestamp}.jpg"
    filepath = cat_photos_dir / filename

    if message:
        url = f"https://cataas.com/cat/says/{requests.utils.quote(message)}"
    else:
        url = "https://cataas.com/cat"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            session_images.append(str(filepath))
            image = Image.open(filepath)
            image.show()
            messagebox.showinfo("Success", f"Saved cat image to: {filepath}")
        else:
            messagebox.showerror("Error", f"Failed to fetch cat image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_submit():
    message = entry.get().strip()
    fetch_and_save_cat_image(message)

def open_cat_photos_folder():
    folder_path = get_cat_photos_dir()
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux and others
            subprocess.run(["xdg-open", folder_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open folder: {e}")

# Set up the GUI
root = tk.Tk()
root.title("Cat Image Downloader")
root.geometry("400x200")

label = tk.Label(root, text="Enter a message for the cat:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

submit_button = tk.Button(root, text="Get Cat Image", command=on_submit)
submit_button.pack(pady=5)

open_folder_button = tk.Button(root, text="Open Cat Photos Folder", command=open_cat_photos_folder)
open_folder_button.pack(pady=5)

root.mainloop()