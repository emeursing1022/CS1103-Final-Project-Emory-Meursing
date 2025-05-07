# -*- coding: utf-8 -*-
"""
@author: Emory Meursing

Summary:
    Code is designed to make an API call to cataas.com to grab a cat photo, with or without a message the user added. The program will prompt the user whether 
    they want the cat to say something, to continue gathering cat photos, to stop the program, or to search through all cat photos gathered in the session. 
    The code uses a class structure to handle all logic, with different methods being used for the API call itself, prompting the user to see if they want
    the cat photo to say something, searching through the session's photos, and prompting the user to continue/end/search.

Directions:
    1) Start the code
    2) Input the message you would like the cat to say (or lackthereof)
    3) See the funny cat
    4) Be questioned on whether you would like to see more funny cats
    	a) If you want to see more funny cats, say yes
    	b) If not, say no, and the program will end
    	c) If you want to see all the photos from this session, you may input any piece of the jpg's name into the "search" function and find all relevant results
    	d) Any other input will result in this question being repeated
"""

import requests
from datetime import datetime
from pathlib import Path
from PIL import Image

class CatAPI:
    USER_INPUT_YES = "yes"
    USER_INPUT_SEARCH = "search"
    USER_INPUT_NO = "no"

    # Set the output directory
    def __init__(self):
        self.session_images = []
        self.desktop = Path.home() / "Desktop"
        self.cat_photos_dir = self.desktop / "cat photos"
        self.cat_photos_dir.mkdir(exist_ok=True)
        self.message = None

    # Prompt the user to input something for the cat to say
    def prompt_for_message(self):
        self.message = input("Would you like the cat to say something? If yes, type the message (or press Enter to skip): ").strip()
        if not self.message:
            self.message = None

    # API call to cataas.com to grab a cat image, with or without a message
    # Also checks for any web errors by making sure the API call returns the code 200
    def fetch_and_save_cat_image(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cat_{timestamp}.jpg"
        filepath = self.cat_photos_dir / filename

        # API call formatting and a check to see if the user wants the cat to say something
        if self.message:
            url = f"https://cataas.com/cat/says/{requests.utils.quote(self.message)}"
        else:
            url = "https://cataas.com/cat"

        # Actual API call, if status code = 200, the API call worked, else it failed to retreive an image
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Saved cat image to: {filepath}")
                Image.open(filepath).show()
                self.session_images.append(str(filepath))
            else:
                print(f"Failed to fetch cat image. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    # See if the user wants to continue or search through the images they've generated this session
    def prompt_for_next_action(self):
        while True:
            action = input("Would you like to download another cat image? (yes/no/search): ").strip().lower()
            if action in [self.USER_INPUT_YES, self.USER_INPUT_SEARCH, self.USER_INPUT_NO]:
                return action
            else:
                print("Please input a valid option: yes, no, or search.")

    # Search through the images generated in this session
    def search(self):
        if not self.session_images:
            print("No images in this session.")
            return

        search_term = input("Enter part of the filename to search for: ").strip().lower()
        matches = [img for img in self.session_images if search_term in img.lower()]

        # Shows all matches based on the user's query
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
    catAPI = CatAPI()
    catAPI.prompt_for_message()
    catAPI.fetch_and_save_cat_image()

    # While the user is in the code, ask them if they would like to continue, search through photos found in that session, or exit
    while True:
        action = catAPI.prompt_for_next_action()
        if action == catAPI.USER_INPUT_YES:
            catAPI.prompt_for_message()
            catAPI.fetch_and_save_cat_image()
        elif action == catAPI.USER_INPUT_SEARCH:
            catAPI.search()
        else:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
