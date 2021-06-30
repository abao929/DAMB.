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

# start = time.time()

# client_id = '36939ed42fef4a33b670d4a6b6b64db7'
# client_secret = '620a5965374c4330b418b277cd522183'

#url = 'https://open.spotify.com/playlist/348iMtCvYQQdICvrxIBbbe?si=GbdYjuDkQ7GtMV-R2cZ98Q' #kofc
# url = 'https://open.spotify.com/playlist/5USCz2dkmTbJ3nLhk4UVip?si=UnYZdZeHQH-4MGsE0Iz0SA' #not like the other
#url = 'https://open.spotify.com/playlist/1LKVe8ZEmFlxlCjqi8Us82?si=BwhGCvPuT02rjc0WQrIpFA' # 20 deloreans
#url = 'https://open.spotify.com/playlist/1na8htLAvxOM3cWLuaublx?si=_vKbFl78S5WWJ8XIfhFhQg' #bossman
#url = 'https://open.spotify.com/playlist/2GI6Z1IZIlsI2KCAECxBj0?si=rqJItCgnTJ6VddPYTZThCw' #sadge
#url = 'https://open.spotify.com/playlist/4XpLccSePOM5xUvsKhkitA?si=nWoxhRJ5ShSWOZV4fxMzzg' #ncs
# page = urllib.request.urlopen(url)
# soup = bs(page, 'html.parser')
# soup = str(soup)

# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# headers = {'User-Agent': user_agent,}

# bad_urls = []

# COMMON_WORDS = ["a", "about", "all", "also", "and", "as", "at", "be", "because", "but", "by", "can", "come", "could", "day", "do", "even", "find", "first",
#  "for", "from", "get", "give", "go", "have", "he", "her", "here", "him", "his", "how", "i", "if", "im", "in", "into", "it", "its", "just", "know", "like", "look",
#  "make", "man", "many", "me", "more", "my", "new", "no", "not", "now", "of", "on", "one", "only", "or", "other", "our", "out", "people", "say", "see", "she",
#  "so", "some", "take", "tell", "than", "that", "the", "their", "them", "then", "there", "these", "they", "thing", "think", "this", "those", "time", "to", "two",
#  "up", "use", "very", "want", "way", "we", "well", "what", "when", "which", "who", "will", "with", "would", "year", "you", "your"]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

#new api stuff
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

def get_genre(access_token):
    url = f'https://api.spotify.com/v1/search?q=lil%20genre:%22southern%20hip%20hop%22&type=album'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    r = requests.get(url, headers=headers).json()
    print(r.keys())
    print(r['albums'])
    albums = []
    return albums

# token = get_token(client_id, client_secret)

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
    r = requests.get(url, headers=headers).json()
    # print(r.keys())
    playlist = r['tracks']['items']
    #print(len(playlist))
    print(r['tracks'].keys())
    next_song = r['tracks']['next']
    #print(f'next song is {next_song}')
    while next_song != None:
        r = requests.get(next_song, headers=headers).json()
        playlist.extend(r['items'])
        next_song = r['next']
    return playlist

def get_all_name_and_artist(playlist):
    table = []
    for song in playlist:
        temp = []
        temp.append(song['track']['name'])
        temp.append(song['track']['artists'][0]['name'])
        table.append(temp)
    return table

def cleanup(string):
    string = string.split('-')[0]
    string = string.split(' (')[0]
    string = string.strip()
    string = re.sub(' +', ' ', string)
    string = string.replace(' ', '-')
    string = string.replace('&', 'and')
    string = re.sub('[^A-Za-z0-9-]', '', string)
    return string

def genius_url(name_and_artist):
    return 'https://genius.com/' + cleanup(name_and_artist[1]) + '-' + cleanup(name_and_artist[0]) + '-lyrics'

def scrape_genius(url):
    cycle_time = time.time()
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
    except HTTPError as err:
        if err.code == 404:
            #print(str(url) + 'error')
            bad_urls.append(url)
            return
        else:
            raise
    genius_soup = bs(response, 'html.parser')
    #print(genius_soup)
    p_tag = genius_soup.p
    text = p_tag.get_text()
    text = re.sub(r'\[.*\]', '', text)
    text = re.sub('[\n]', ' ', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    text = text.lower()
    text = text.split()
    scrape_genius.calls += 1
    end_cycle = time.time()
    print(f'spent {end_cycle-cycle_time} seconds on song {scrape_genius.calls}: {url}')
    return text


def everything():
    total_text = []
    all_songs = get_all_name_and_artist(get_playlist('1na8htLAvxOM3cWLuaublx', get_token(client_id, client_secret)))
    #all_songs = get_all_name_and_artist(split_song())
    for pair in all_songs:
        genius_data = scrape_genius(genius_url(pair))
        if genius_data != None:
            #print(genius_data)
            total_text.extend(genius_data)
        #print(total_text)
    filtered_text = filter(lambda s: s not in COMMON_WORDS, total_text)
    print(str(len(all_songs)) + ' songs')
    print(all_songs)
    print(str(len(bad_urls)) + ' invalid urls: ' + str(bad_urls))
    separator = ' '
    return separator.join(filtered_text)
    #return Counter(filtered_text).most_common()

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
        print(info)
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
    for playlist in playlist_codes:
        album_urls, info_list = get_album_covers(get_playlist(playlist, token))
        download_album_covers(album_urls, info_list, genre)


def main():
    # replace with your token here:
    token = "BQBY2xTUjRhyQp87JAOkR4NkzgEF3L-6BVkG7lp8zm6FDhIhmOxJqXoyApVUXl_Kksx0wO22x_y3L_-qdlar0kHVeRnzjCYVys7pQpQC1QcPvCrKX7hPwj21n-2tvBow8cl0fF67-GQg"
    # your playlist codes and genre:
    playlist_codes = ['37i9dQZF1DXbLMw3ry7d7k', '37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DWY6chQMXb0Zh', '37i9dQZF1DWZQkHAMKYFuV', '37i9dQZF1DWZJIhAWlsiOv', '37i9dQZF1DX4g1k3dwPPvk', '37i9dQZF1DWVcbzTgVpNRm']
    # make sure genre is set to the correct one:
    genre = 'latin'
    # get all the album covers from the playlists:
    get_playlists_album_covers(playlist_codes, token, genre)

if __name__ == '__main__':
    main()