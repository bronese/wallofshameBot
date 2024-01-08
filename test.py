import requests
import json
import configparser
import os
import time

config = configparser.ConfigParser()
config.read('config.ini')
folder_name = "artists"
genres=["cloud rap"]

def make_api_call(genre, max_iterations=10):
    offset = 0
    artist_names_decoded = []  # Initialize the list for decoded artist names
    iterations = 0
    while True:
        if iterations >= max_iterations:
            break
        url = f"http://musicbrainz.org/ws/2/artist?query=tag:{genre}&fmt=json&limit=100&offset={offset}"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            print(response.status_code)
            return artist_names_decoded  # Exit the function and return the list
        time.sleep(2)
        artists = data.get('artists', [])  # Safely retrieve the 'artists' key with a default value of an empty list
        for artist in artists:
            artist_names_decoded.append(artist['name'])
        if len(artists) < 100:
            break
# Return the list of artist names
def build_lists(genres):
    totalArtist = 0
    if len(genres) == 1:
        artist_names_decoded = make_api_call(genres[0])
        print(f"making call {genres}")
        file_name = f"{genres[0]}.json"
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write JSON data to the file
            json.dump(artist_names_decoded, file, ensure_ascii=False)
        print(len(artist_names_decoded))
        print(f"{genres[0]} queried to {file_path}")
        totalArtist += len(artist_names_decoded)
    else:
        for genre in genres:
            artist_names_decoded = make_api_call(genre)
            file_name = f"{genre.replace(' ', '_')}.json"
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                # Write JSON data to the file
                json.dump(artist_names_decoded, file, ensure_ascii=False)
            print(len(artist_names_decoded))
            print(f"{genre} queried to {file_path}")
            totalArtist += len(artist_names_decoded)
    print(f"Success {totalArtist} queried!")
build_lists(genres)