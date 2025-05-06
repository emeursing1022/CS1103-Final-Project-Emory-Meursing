# -*- coding: utf-8 -*-
"""
@author: Emory Meursing
"""

import requests
import os
from datetime import datetime
from pathlib import Path
from PIL import Image

def fetch_and_save_cat_image(message=None, session_images=None):
    # Get the user's desktop path
    desktop = Path.home() / "Desktop"
    cat_photos_dir = desktop / "cat photos"
    cat_photos_dir.mkdir(exist_ok=True)

    # Create a unique filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cat_{timestamp}.jpg"
    filepath = cat_photos_dir / filename

    # API endpoint for a random cat image (with optional text)
    if message:
        url = f"https://cataas.com/cat/says/{requests.utils.quote(message)}"
    else:
        url = "https://cataas.com/cat"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Saved cat image to: {filepath}")
            Image.open(filepath).show()
            if session_images is not None:
                session_images.append(str(filepath))
        else:
            print(f"Failed to fetch cat image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def search_images(session_images):
    if not session_images:
        print("No images in this session.")
        return

    search_term = input("Enter part of the filename to search for: ").strip().lower()
    matches = [img for img in session_images if search_term in img.lower()]

    if matches:
        print("Matching images:")
        for i, img in enumerate(matches):
            print(f"[{i}] {img}")

        while True:
            choice = input("Enter the number of an image to open it, or press Enter to cancel: ").strip()
            if choice == "":
                break
            if choice.isdigit():
                index = int(choice)
                if 0 <= index < len(matches):
                    try:
                        Image.open(matches[index]).show()
                        break
                    except Exception as e:
                        print(f"Error opening image: {e}")
                else:
                    print("Invalid selection. Try again.")
            else:
                print("Please enter a valid number or press Enter to cancel.")
    else:
        print("No matches found.")

def main():
    session_images = []
    while True:
        # Ask the user if they want the cat to say something
        message = input("Would you like the cat to say something? If yes, type the message (or press Enter to skip): ").strip()
        fetch_and_save_cat_image(message if message else None, session_images)

        while True:
            cont = input("Would you like to download another cat image? (yes/no/search): ").strip().lower()
            if cont == "no":
                print("Goodbye!")
                return
            elif cont == "search":
                search_images(session_images)
            elif cont != "yes":
                print("Please input a proper value.")
            else:
                break

if __name__ == "__main__":
    main()


