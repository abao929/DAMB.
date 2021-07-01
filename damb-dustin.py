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

def get_token(client_id, client_secret):
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

def get_album_covers(playlist):
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
        artist = album['artists'][0]['name']
        name = album['name']
        cover_url = album['images'][0]['url']
        album_url  = album['external_urls']['spotify']
        info_list += [[name, artist, cover_url, album_url]]

        if cover_url not in album_list:
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
    for link, info in zip(cover_urls, info_list):
        album_name, artist, _, _ = info
        album_name = album_name.replace("/", '-').replace(' ', '-')
        artist = artist.replace("/", '-').replace(' ', '-')
        
        filename = f'{genre}/{album_name}-{artist}.jpg'
        urllib.request.urlretrieve(link, filename)
        

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
        album_urls, info_list = get_album_covers(get_playlist(playlist, token))
        all_albums += album_urls
        all_infos += info_list

    # remove duplicate tracks
    all_album_info_pairs = list(zip(all_albums, all_infos))
    unique_album_info_pairs = list(dict(all_album_info_pairs).items())
    unique_albums = [pair[0] for pair in unique_album_info_pairs]
    unique_infos = [pair[1] for pair in unique_album_info_pairs]

    download_album_covers(unique_albums, unique_infos, genre)

    # write a csv consisting of track info
    with open(genre + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'artist', 'cover_url', 'album_url'])
        writer.writerows(unique_infos)

def main():
    token = get_token('ddca8689d9204ea9b5cc65950a0d6ae1', '5f31abfff68d4017926f7eb2eaf179da')
    # make sure genre is set to the correct one
    # note that playlists should only consist of songs of the correct genre. You can look up a genre on spotify to search for playlists.

    # genre = 'metal'
    # playlist_codes = ['37i9dQZF1DWWOaP4H0w5b0', '37i9dQZF1DX9qNs32fujYe', '37i9dQZF1DWTcqUzwhNmKv', '37i9dQZF1DWXHwQpcoF2cC', '37i9dQZF1DWUnhhRs5u3TO', '37i9dQZF1EQpgT26jgbgRI']

    # genre = 'pop'
    # playlist_codes = ['37i9dQZF1EQncLwOalG3K7', '5TDtuKDbOhrfW7C58XnriZ', '6mtYuOxzl58vSGnEDtZ9uB', '37i9dQZF1DWXti3N4Wp5xy', '37i9dQZF1DWUa8ZRTfalHk', '37i9dQZF1DXcOFePJj4Rgb']

    # genre = 'r-n-b'
    # playlist_codes = ['37i9dQZF1EQoqCH7BwIYb7', '37i9dQZF1DX04mASjTsvf0', '37i9dQZF1DX6VDO8a6cQME', '37i9dQZF1DWXbttAJcbphz', '37i9dQZF1DWYmmr74INQlb', '37i9dQZF1DX7FY5ma9162x', '7Ll3CWx8VwRan0FFamai5X']

    #genre = 'rock'
    #playlist_codes = ['37i9dQZF1DWXRqgorJj26U', '37i9dQZF1EQpj7X7UK8OOF', '37i9dQZF1DWWJOmJ7nRx0C', '37i9dQZF1DX8FwnYE6PRvL', '37i9dQZF1DX7Ku6cgJPhh5', '37i9dQZF1DWYctfAtweUtE']

    #genre = 'edm'
    #playlist_codes = ['37i9dQZF1DX1kCIzMYtzum', '37i9dQZF1DX8tZsk68tuDw', '37i9dQZF1DX4dyzvuaRJ0n', '37i9dQZF1DX6J5NfMJS675', '37i9dQZF1DX572PAi3rtlM', '37i9dQZF1DXa8NOEUWPn9W']
    
    #genre = 'heavy-metal'
    #playlist_codes = ['37i9dQZF1DX9qNs32fujYe', '6f36ma26ZFVQJ5ENPCTmYM', '2V3VUo9eHiEZRpBOcOIWeY', '44nvE1PZwr2EAE5NaqwbbX', '4xySBwCetTFl3XFjPeLRKA']

    genre = 'hip-hop'
    playlist_codes = ['37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX6GwdWRQMQpq', '37i9dQZF1DWY4xHQp97fN6', '37i9dQZF1DX2RxBh64BHjQ', '37i9dQZF1DX9oh43oAzkyx', '37i9dQZF1DX76t638V6CA8', '37i9dQZF1DX7Mq3mO5SSDc', '37i9dQZF1DWT5MrZnPU1zD']
    
    # get all the album covers from the playlists:
    
    get_playlists_album_covers(playlist_codes, token, genre)

if __name__ == '__main__':
    main()