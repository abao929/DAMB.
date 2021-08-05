from bs4 import BeautifulSoup as bs
import urllib.request
from urllib.error import HTTPError
import csv
import re
import requests
from collections import Counter
import base64
import datetime
import time
import os
import random
from itertools import zip_longest

def get_token(client_id, client_secret):
    '''
    given a Spotify API client id, and client secret, returns a Spotify API
    token to make requests from. Each token has a limited period before it
    expires so this function ensures that we always generate a new token
    during each run
    :param client_id: string representing a client id from Spotify's API developer console
    :param client_secret: string representing a client secret from Spotify's API developer console
    '''
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = { 
        'grant_type': 'client_credentials'
    }
    client_creds = f'{client_id}:{client_secret}'
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_headers = {
        'Authorization': f'Basic {client_creds_b64.decode()}'
    }
    r = requests.post(token_url, data=token_data, headers=token_headers)
    valid_request = r.status_code in range (200, 299)
    if valid_request:
        token_response_data = r.json()
        return token_response_data['access_token']
    return

def get_playlist(playlist_id, access_token):
    '''
    given a playlist id, returns the playlist's dictionary of information for each song
    :param playlist_id: string of playlist id
    :param access_token: api token
    '''
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # print(url)

    req = requests.get(url, headers=headers)
    r = req.json()
    # print(r.keys(), r.values())
    playlist = r['tracks']['items']
    #print(len(playlist))
    # print(r['tracks'].keys())
    next_song = r['tracks']['next']
    #print(f'next song is {next_song}')
    while next_song != None:
        r = requests.get(next_song, headers=headers).json()
        playlist.extend(r['items'])
        next_song = r['next']
    return playlist

def process_playlist(playlist, genre, access_token):
    track_infos = []
    for entry in playlist:
        track_dict = entry['track']
        album_dict = track_dict['album']

        album_id = album_dict['id']
        album_name = album_dict['name']
        album_name = album_name.replace("/", '-').replace(' ', '-')
        artist = album_dict['artists'][0]['name']
        artist = artist.replace("/", '-').replace(' ', '-')
        # album_url  = album_dict['external_urls']['spotify'].lower()
        # cover_url = album_dict['images'][0]['url'].lower()
        cover_location = os.path.join(genre, album_name + '-' + artist + '.jpg')
        cover_location = cover_location[:-4][:251] + '.jpg'
        cover_location = os.path.join('image-data', cover_location)

        track_id = track_dict['id']
        track_name = track_dict['name']
        track_name = track_name.replace("/", '-').replace(' ', '-')
        popularity = track_dict['popularity']
        explicit = track_dict['explicit']

        track_info = [album_id, album_name, cover_location, artist, track_id, track_name, popularity, explicit]
        track_infos.append(track_info)
    
    return track_infos

def get_audio_info(tracks_chunk, access_token):
    audio_infos = []
    tracks_chunk = [x for x in tracks_chunk if x is not None]
    track_ids = [track_info[4] for track_info in tracks_chunk]
    tracks_str = ','.join(track_ids)
    payload = {'ids': tracks_str}

    request_audio_features_url = f'https://api.spotify.com/v1/audio-features'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    audio_features_response = requests.get(request_audio_features_url, params=payload, headers=headers)
    audio_features_dicts = audio_features_response.json()['audio_features']

    for audio_features_dict in audio_features_dicts:
        if audio_features_dict == None:
            audio_infos.append([])
        else:
            danceability = audio_features_dict['danceability']
            energy = audio_features_dict['energy']
            key = audio_features_dict['key']
            loudness = audio_features_dict['loudness']
            modality = audio_features_dict['mode']
            valence = audio_features_dict['valence']
            speechiness = audio_features_dict['speechiness']

            audio_info = [danceability, energy, key, loudness, modality, valence, speechiness]
            audio_infos.append(audio_info)
    
    return audio_infos

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def main():
    # Obtain our Spotify API token that we will use to make queries
    token = get_token('ddca8689d9204ea9b5cc65950a0d6ae1', '5f31abfff68d4017926f7eb2eaf179da')

    # These are the genres that we will collect data for
    genres = ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative', 'blues', 'classical', 'country']
    # Each string is an ID corresponding to a Spotify-generated or user-genereated playlist that is dedicated to songs of a specific genre. These were found manually
    # by all members of our group.
    playlist_codes_dict = {
        'metal': ['37i9dQZF1DWWOaP4H0w5b0', '37i9dQZF1DX9qNs32fujYe', '37i9dQZF1DWTcqUzwhNmKv', '37i9dQZF1DWXHwQpcoF2cC', '37i9dQZF1DWUnhhRs5u3TO', '37i9dQZF1EQpgT26jgbgRI', '37i9dQZF1DWXNFSTtym834', '37i9dQZF1DX08jcQJXDnEQ', '7wzZTz1XYoruUJFHV8MZB6', '37i9dQZF1DX6P51sFpSo2r', '37i9dQZF1DXbyrUWMp2Tkr'],
        'pop': ['37i9dQZF1EQncLwOalG3K7', '5TDtuKDbOhrfW7C58XnriZ', '6mtYuOxzl58vSGnEDtZ9uB', '37i9dQZF1DWXti3N4Wp5xy', '37i9dQZF1DWUa8ZRTfalHk', '37i9dQZF1DXcOFePJj4Rgb', '37i9dQZF1DX7IEQm3xNsaz', '3JoHkM90TXzfIS1RMN0Cgd'],
        'r-n-b': ['37i9dQZF1EQoqCH7BwIYb7', '37i9dQZF1DX04mASjTsvf0', '37i9dQZF1DX6VDO8a6cQME', '37i9dQZF1DWXbttAJcbphz', '37i9dQZF1DWYmmr74INQlb', '37i9dQZF1DX7FY5ma9162x', '7Ll3CWx8VwRan0FFamai5X', '37i9dQZF1DX2UgsUIg75Vg', '37i9dQZF1DX2WkIBRaChxW', '1kMyrcNKPws587cSAOjyDP'],
        'rock': ['37i9dQZF1DWXRqgorJj26U', '37i9dQZF1EQpj7X7UK8OOF', '37i9dQZF1DWWJOmJ7nRx0C', '37i9dQZF1DX8FwnYE6PRvL', '37i9dQZF1DX7Ku6cgJPhh5', '37i9dQZF1DWYctfAtweUtE', '37i9dQZF1DX49jUV2NfGku', '37i9dQZF1DX3YMp9n8fkNx', '37i9dQZF1DX1te6miphixI'],
        'edm': ['37i9dQZF1DX1kCIzMYtzum', '37i9dQZF1DX8tZsk68tuDw', '37i9dQZF1DX4dyzvuaRJ0n', '37i9dQZF1DX6J5NfMJS675', '37i9dQZF1DX572PAi3rtlM', '37i9dQZF1DXa8NOEUWPn9W', '09T8BRorjn8It7gCCKuT3U', '5aEYhFPmLG3fHcOgv3NeEK', '5XoGCyXu8TWiHZ701KkhZa'],
        'hip-hop': ['37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX6GwdWRQMQpq', '37i9dQZF1DWY4xHQp97fN6', '37i9dQZF1DX2RxBh64BHjQ', '37i9dQZF1DX9oh43oAzkyx', '37i9dQZF1DX76t638V6CA8', '37i9dQZF1DX7Mq3mO5SSDc', '37i9dQZF1DWT5MrZnPU1zD', '37i9dQZF1DWUFmyho2wkQU', '0weizyV5WNZP3tvfXWVfmg'],
        'indie': ['37i9dQZF1DX2Nc3B70tvx0', '37i9dQZF1DX2NwU6NbPUdo', '37i9dQZF1DWUoqEG4WY6ce', '37i9dQZF1EQqkOPvHGajmW', '37i9dQZF1DX9LbdoYID5v7', '3qyQ76WcXIIOINuGVLyoEp', '2GZcWuiiTXJr7neZFF63rX', '37i9dQZF1DXdbXrPNafg9d', '37i9dQZF1DWYBF1dYDPlHw'],
        'jazz': ['37i9dQZF1DWTKxc7ZObqeH', '37i9dQZF1DX9GSZDbrndTa', '37i9dQZF1DWTbzY5gOVvKd', '37i9dQZF1EQqA6klNdJvwx', '37i9dQZF1DX76YsWjvbz9I', '37i9dQZF1DXbHcQpOiXk1D', '37i9dQZF1DWTR4ZOXTfd9K', '37i9dQZF1DX1S1NduGwpsa', '37i9dQZF1DXdwTUxmGKrdN', '37i9dQZF1DWVqfgj8NZEp1', '37i9dQZF1DX71VcjjnyaBQ', '37i9dQZF1DWWMGLiuK4OqL'],
        'kpop': ['37i9dQZF1DX9tPFwDMOaN1', '37i9dQZF1DX4FcAKI5Nhzq', '37i9dQZF1DX8NzI27ip7J0', '37i9dQZF1DX6Cy4Vr7Hu2y', '37i9dQZF1DWUoY6Ih7vsxr', '37i9dQZF1DWZYjbSZYSpu6', '37i9dQZF1DXe5W6diBL5N4', '2EoheVFjqIxgJMb8VnDRtZ', '66akWBDmzVkfuKHSgbuens'],
        'latin': ['37i9dQZF1DXbLMw3ry7d7k', '37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DWY6chQMXb0Zh', '37i9dQZF1DWZQkHAMKYFuV', '37i9dQZF1DWZJIhAWlsiOv', '37i9dQZF1DX4g1k3dwPPvk', '37i9dQZF1DWVcbzTgVpNRm','37i9dQZF1DX3omIq8ziEt6', '37i9dQZF1DX5y71ufjoyXC', '37i9dQZF1DWYK2yx0OW9Kj'],
        'alternative': ['37i9dQZF1DX9GRpeH4CL0S', '37i9dQZF1DX873GaRGUmPl', '5G54gG9eqXXGQAHVHGzloP', '5jKkHPUXGZHitWujNXQREE', '3ISON95lf4mB2ZY1JFB7lt'],
        'blues': ['37i9dQZF1DXd9rSDyQguIk', '6ufJ2nIUqkjkX1SagjI2kw', '5TkTomPbQuSNDxdlWg2fCx', '56dbowk1V5ycS5jW7DSvi5', '37i9dQZF1DWSKpvyAAcaNZ', '37i9dQZF1DX0QNpebF7rcL', '37i9dQZF1DXcu3QLJudo4X', '37i9dQZF1DX1STMhgdmNBY', '37i9dQZF1DX8QB9Ys2nV17'],
        'classical': ['1h0CEZCm6IbFTbxThn6Xcs', '37i9dQZF1DWVFeEut75IAL', '37i9dQZF1DWWEJlAGA9gs0', '37i9dQZF1DXd5zUwdn6lPb', '29TfHADnSx2AvDSgbWBMDU', '2bKGFDfzL8eD9XgH4IsQPC', '5ifMsPihlkYEGCakqfqj17', '1Z7fO3bkVteGsTbVluOQoH'],
        'country': ['7lQu0IRGR1qTjWYdZbbKXE', '0J74JRyDCMotTzAEKMfwYN', '37i9dQZF1DX13ZzXoot6Jc', '37i9dQZF1DXdxUH6sNtcDe', '37i9dQZF1DWXdiK4WAVRUW', '37i9dQZF1DX8WMG8VPSOJC']
    }
    # Create a directory to store our data in
    data_path = 'data'
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    data = []

    for genre in genres:
        playlist_codes = playlist_codes_dict[genre]

        track_data = []
        for playlist_code in playlist_codes:
            print(playlist_code)
            playlist = get_playlist(playlist_code, token)
            track_infos = process_playlist(playlist, genre, token)
            track_data += track_infos

        audio_data = []
        for tracks_chunk in grouper(track_data, 100):
            audio_data += get_audio_info(tracks_chunk, token)

        for i in range(len(track_data)):
            data.append(track_data[i] + audio_data[i] + [genre])

    header = ['album_id', 'album_name', 'cover_location', 'artist', 'track_id', 'track_name', 'popularity', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'modality', 'valence', 'speechiness', 'genre']
    data = [row for row in data if (row != None) and (len(row) == len(header))]

    random.shuffle(data)
    n = len(data)
    n_test = n // 5 # 80-20 split
    data_train = data[n_test:]
    data_test = data[:n_test]

    with open(os.path.join(data_path, 'data-train-final-final.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_train)
    
    with open(os.path.join(data_path, 'data-test-final-final.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_test)



if __name__ == '__main__':
    main()