import requests
import json
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
folder_name = "artists"
folder_path = f"{folder_name}/"
genres_str = config['GENERAL']['Genres']
genres = genres_str.split(', ')

def search_artists_by_genre(genre):
    totalArtist = 0
    if not os.path.exists(folder_name):
        # Create the folder
        os.makedirs(folder_name)
        print(f"The '{folder_name}' folder has been created.")
    else:
        print(f"The '{folder_name}' folder already exists.")
    for genre in genres:
        genre_quoted = f'"{genre}"'  # Add quotes around the genre
        artist_names_decoded = []  # Initialize the list for decoded artist names
        offset = 0
        while True:
            url = f"http://musicbrainz.org/ws/2/artist?query=tag:{genre_quoted}&fmt=json&limit=100&offset={offset}"
            response = requests.get(url)
            data = response.json()
            artists = data.get('artists', [])  # Safely retrieve the 'artists' key with a default value of an empty list
            for artist in artists:
                artist_names_decoded.append(artist['name'])
            if len(artists) < 100:
                break
            offset += len(artists)
        file_name = f"{genre.replace(' ','_')}.json"
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write JSON data to the file
            json.dump(artist_names_decoded, file, ensure_ascii=False)
            print(f"{len(artist_names_decoded)} total number artists")
            print(f"{genre} queried to {file_path}")
        # Iterate over the files in the folder
    for name in os.listdir(folder_path):  # Update the argument to folder_path
        file_path = os.path.join(folder_path, name)
            # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Count the number of artists in the JSON file
        totalArtist += len(data)  # Update the variable name to totalArtist
    print(f"{totalArtist} artists loaded")

def write_artists():
    config.read('config.ini')
    file_path = f'{folder_path}/customartist.json'
    custom_artists = config['GENERAL']['individualartists']
    custom_artists_list = custom_artists.split(',')  # Split the string into a list of artists
    with open(file_path, 'w') as file:
        json.dump(custom_artists_list, file)