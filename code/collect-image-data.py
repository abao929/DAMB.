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
    r = requests.get(url, headers=headers).json()
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

def get_album_covers(playlist, genre):
    '''
    given the playlist dictionary of information, returns a list of album-cover-urls
    :param playlist: a playlist dictionary of information
    :return: a list of album-cover-urls, a list of corresponding album cover information
        where each album's info includes [album name, artist, cover url, album url]
    '''
    album_list = []
    info_list = []
    for song in playlist:
        # album_info = []
        album = song['track']['album']
        artist = album['artists'][0]['name'].lower()
        name = album['name'].lower()
        if len(album['images']) == 0:
            continue
        cover_url = album['images'][0]['url'].lower()
        album_url  = album['external_urls']['spotify'].lower()

        album_name = name.replace("/", '-').replace(' ', '-')
        artist = artist.replace("/", '-').replace(' ', '-')
        filename = os.path.join(genre, album_name + '-' + artist + '.jpg')

        info_list += [[name, artist, cover_url, album_url, filename]]

        album_list.append(cover_url)

    return album_list, info_list


def download_album_covers(cover_urls, info_list, genre):
    '''
    given a list of album cover urls, saves each image in the genre folder
    :param cover_urls: a list of cover urls
    :param info_list: a list of corresponding album information [album name, artist, cover url, spotify url]
    :param genre: a string of the genre name
    :return: nothing
    '''
    album_filenames = []
    
    for link, info in zip(cover_urls, info_list):
        filename = info[4]
        album_filenames.append(filename)
        urllib.request.urlretrieve(link, os.path.join('image_data', filename[:-4][:251] + '.jpg'))
    
    return
        

def get_playlists_album_covers(playlist_codes, token, genre):
    '''
    given a list of playlist codes, saves all the album covers of the songs in all of the playlists
    :param playlist_codes: a list of playlist codes (strings)
    :param token: api token
    :param genre: string of the genre name
    '''
    all_albums = []
    all_infos = []

    for playlist in playlist_codes:
        album_urls, info_list = get_album_covers(get_playlist(playlist, token), genre)
        all_albums += album_urls
        all_infos += info_list

    download_album_covers(all_albums, all_infos, genre)

    # write a csv consisting of track info
    with open(os.path.join('image_data', genre + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(['name', 'artist', 'cover_url', 'album_url', 'album_path'])
        seen = set()
        unique_rows = []
        for row in map(tuple, all_infos):
            if not row[0] in seen:
                seen.add(row[0])
                unique_rows.append(row)

        unique_rows.sort()
        writer.writerows(unique_rows)


def main():
    # Obtain our Spotify API token that we will use to make queries
    token = get_token('ddca8689d9204ea9b5cc65950a0d6ae1', '5f31abfff68d4017926f7eb2eaf179da')

    # These are the genres that we will collect data for
    genres = ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'heavy-metal', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative', 'blues', 'classical', 'country']

    # Each string is an ID corresponding to a Spotify-generated or user-genereated playlist that is dedicated to songs of a specific genre. These were found manually
    # by all members of our group.
    playlist_codes_dict = {
        'metal': ['37i9dQZF1DWWOaP4H0w5b0', '37i9dQZF1DX9qNs32fujYe', '37i9dQZF1DWTcqUzwhNmKv', '37i9dQZF1DWXHwQpcoF2cC', '37i9dQZF1DWUnhhRs5u3TO', '37i9dQZF1EQpgT26jgbgRI'],
        'pop': ['37i9dQZF1EQncLwOalG3K7', '5TDtuKDbOhrfW7C58XnriZ', '6mtYuOxzl58vSGnEDtZ9uB', '37i9dQZF1DWXti3N4Wp5xy', '37i9dQZF1DWUa8ZRTfalHk', '37i9dQZF1DXcOFePJj4Rgb'],
        'r-n-b': ['37i9dQZF1EQoqCH7BwIYb7', '37i9dQZF1DX04mASjTsvf0', '37i9dQZF1DX6VDO8a6cQME', '37i9dQZF1DWXbttAJcbphz', '37i9dQZF1DWYmmr74INQlb', '37i9dQZF1DX7FY5ma9162x', '7Ll3CWx8VwRan0FFamai5X'],
        'rock': ['37i9dQZF1DWXRqgorJj26U', '37i9dQZF1EQpj7X7UK8OOF', '37i9dQZF1DWWJOmJ7nRx0C', '37i9dQZF1DX8FwnYE6PRvL', '37i9dQZF1DX7Ku6cgJPhh5', '37i9dQZF1DWYctfAtweUtE'],
        'edm': ['37i9dQZF1DX1kCIzMYtzum', '37i9dQZF1DX8tZsk68tuDw', '37i9dQZF1DX4dyzvuaRJ0n', '37i9dQZF1DX6J5NfMJS675', '37i9dQZF1DX572PAi3rtlM', '37i9dQZF1DXa8NOEUWPn9W'],
        'heavy-metal': ['37i9dQZF1DX9qNs32fujYe', '6f36ma26ZFVQJ5ENPCTmYM', '2V3VUo9eHiEZRpBOcOIWeY', '44nvE1PZwr2EAE5NaqwbbX', '4xySBwCetTFl3XFjPeLRKA'],
        'hip-hop': ['37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX6GwdWRQMQpq', '37i9dQZF1DWY4xHQp97fN6', '37i9dQZF1DX2RxBh64BHjQ', '37i9dQZF1DX9oh43oAzkyx', '37i9dQZF1DX76t638V6CA8', '37i9dQZF1DX7Mq3mO5SSDc', '37i9dQZF1DWT5MrZnPU1zD'],
        'indie': ['37i9dQZF1DX2Nc3B70tvx0', '37i9dQZF1DX2NwU6NbPUdo', '37i9dQZF1DWUoqEG4WY6ce', '37i9dQZF1EQqkOPvHGajmW', '37i9dQZF1DX9LbdoYID5v7'],
        'jazz': ['37i9dQZF1DWTKxc7ZObqeH', '37i9dQZF1DX9GSZDbrndTa', '37i9dQZF1DWTbzY5gOVvKd', '37i9dQZF1EQqA6klNdJvwx', '37i9dQZF1DX76YsWjvbz9I', '37i9dQZF1DXbHcQpOiXk1D', '37i9dQZF1DWTR4ZOXTfd9K', '37i9dQZF1DX1S1NduGwpsa'],
        'kpop': ['37i9dQZF1DX9tPFwDMOaN1', '37i9dQZF1DX4FcAKI5Nhzq', '37i9dQZF1DX8NzI27ip7J0', '37i9dQZF1DX6Cy4Vr7Hu2y', '37i9dQZF1DWUoY6Ih7vsxr', '37i9dQZF1DX1LU4UHKqdtg', '37i9dQZF1DWZYjbSZYSpu6', '37i9dQZF1DXe5W6diBL5N4'],
        'latin': ['37i9dQZF1DXbLMw3ry7d7k', '37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DWY6chQMXb0Zh', '37i9dQZF1DWZQkHAMKYFuV', '37i9dQZF1DWZJIhAWlsiOv', '37i9dQZF1DX4g1k3dwPPvk', '37i9dQZF1DWVcbzTgVpNRm'],
        'alternative': ['37i9dQZF1DX9GRpeH4CL0S', '37i9dQZF1DX873GaRGUmPl', '5G54gG9eqXXGQAHVHGzloP', '5jKkHPUXGZHitWujNXQREE', '3ISON95lf4mB2ZY1JFB7lt', '2HygMjjtUsZJeooZoQ8oMB'],
        'blues': ['37i9dQZF1DXd9rSDyQguIk', '6ufJ2nIUqkjkX1SagjI2kw', '5TkTomPbQuSNDxdlWg2fCx', '56dbowk1V5ycS5jW7DSvi5', '37i9dQZF1DWSKpvyAAcaNZ', '37i9dQZF1DX0QNpebF7rcL'],
        'classical': ['1h0CEZCm6IbFTbxThn6Xcs', '37i9dQZF1DWVFeEut75IAL', '37i9dQZF1DWWEJlAGA9gs0', '37i9dQZF1DXd5zUwdn6lPb', '29TfHADnSx2AvDSgbWBMDU', '2bKGFDfzL8eD9XgH4IsQPC', '5ifMsPihlkYEGCakqfqj17', '1Z7fO3bkVteGsTbVluOQoH', '3tzZNGemkwbXFH6T6r4ElA', '2IUEKduilh9DtH1WFzOZ07', '0CcBreFuJdFY10TZmSN2Ws'],
        'country': ['7lQu0IRGR1qTjWYdZbbKXE', '0J74JRyDCMotTzAEKMfwYN', '37i9dQZF1DX13ZzXoot6Jc', '37i9dQZF1DXdxUH6sNtcDe', '37i9dQZF1DWXdiK4WAVRUW', '41atVM1CMCAmZ62euTrCla', '6wQFfOF4QYyoZhBGlhCWHZ']
    }

    # Create a directory to store our data in
    if not os.path.exists('image_data'):
        os.mkdir('image_data')

    # For each genre, open each playlist and download the album covers of each song's album
    for genre in genres:
        if not os.path.exists(os.path.join('image_data', genre)):
            os.mkdir(os.path.join('image_data', genre))
        
        playlist_codes = playlist_codes_dict[genre]

        get_playlists_album_covers(playlist_codes, token, genre)

if __name__ == '__main__':
    main()