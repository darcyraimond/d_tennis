# Functionality for player static information to be stored and retrieved
# (this is information about a player at the time of the match)


# Import any required packages
from termcolor import colored
import os
import requests
from .data_loader import load


# ==================================================
# Content below this point
# ==================================================


def clean(folder_name):
    os.system(f"rm -rf {folder_name}")


def request_to_file(request, file_name, folder_name):
    #os.system(f"touch {folder_name}/atp_players.csv")
    with open(f"{folder_name}/{file_name}", "w") as file:
        content = str(request.content).replace("\\'", "'").split("\\n")
        if content[0][0:2] == "b'" or content[0][0:2] == 'b"':
            content[0] = content[0][2:]
        if content[-1] == "'" or content[-1] == '"':
            content = content[:-1]
        l = len(content)
        for i, line in enumerate(content):
            file.write(line)
            file.write("\n")


def download_files(silent = False):

    if not silent:
        print(colored("Downloading data...", "blue"))

    try:

        # Basics
        base_url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"
        folder_name = "tennis_atp-master"

        # Running this first ensures connection issues realised before old dataset deleted
        data = requests.get(f"{base_url}atp_players.csv")

        # Create initial folder
        clean(folder_name)
        os.system(f"mkdir {folder_name}")

        # Add player data
        if not silent:
            print(colored("Up to file: atp_players.csv     ", "blue"), end = "\r")
        request_to_file(data, "atp_players.csv", folder_name)

        # Add match data
        year = 1968
        file_name = f"atp_matches_{year}.csv"
        data = requests.get(f"{base_url}{file_name}")
        while data.status_code == 200:
            if not silent:
                print(colored(f"Up to file: {file_name}     ", "blue"), end = "\r")
            request_to_file(data, file_name, folder_name)
            year += 1
            file_name = f"atp_matches_{year}.csv"
            data = requests.get(f"{base_url}{file_name}")

        if not silent:
            print(colored("Finished downloading files             ", "blue"))
        
    except requests.exceptions.ConnectionError:
        print(colored("Fatal Error:", "red"), "unable to establish connection,", 
                "consider using a local dataset (if available) with load(path).",
                "Alteriatnvely, if the dataset has been downloaded before using load_auto, try load_auto(force_new_download = False)")
        exit(1)


def load_auto(force_new_download=False, silent=False):

    path = "tennis_atp-master/"

    if force_new_download:
        download_files(silent)
        load(path, silent)
    else:
        # Check if a copy is already downloaded
        try:
            load(path, silent)
        except FileNotFoundError:
            if not silent:
                print(colored("Could not find required files, attempting to download", "blue"))
            download_files(silent)
            load(path, silent)