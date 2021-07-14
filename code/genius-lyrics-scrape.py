import os
import re
import lyricsgenius as lg
import pandas as pd

GENIUS_API_TOKEN = 'ygRZEqplSNX4bqaDP4SGBG2ZtMgIMg7j7Qt26RIYw-6IQy_Ie_Qw2ONkF2rxcpti'
genius = lg.Genius(GENIUS_API_TOKEN)

def clean_song_artist_names(song_name, artist):
    artist_name_list = artist.split('-')
    paren_location = song_name.find('(')
    if paren_location != -1:
        song_name = song_name[:paren_location]
    song_name_list = song_name.split('-')
    
    artist = ''
    song = ''
    for i in range(len(artist_name_list)):
        if artist_name_list[i] != '':
            artist_string = artist_name_list[i]
            artist_string = artist_string.replace('&', 'and')
            artist_string = re.sub(' +', ' ', artist_string)
            # artist_string = re.sub('[^A-Za-z0-9-]', '', artist_string)
            artist += artist_string
            artist += ' '
    
    for i in range(len(song_name_list)):
        if song_name_list[i] != '':
            song_string = song_name_list[i]
            song_string = song_string.replace('&', 'and')
            song_string = re.sub(' +', ' ', song_string)
            # song_string = re.sub('[^A-Za-z0-9-]', '', song_string)
            song += song_string
            song += ' '
    if song[-1] == ' ':
        song = song[:-1]
    if artist[-1] == ' ':
        artist = artist[:-1]

    return song, artist

def get_song_lyrics(song_name, artist_name):
    song = genius.search_song(song_name, artist_name)
    if song is None:
        lyrics = ''
    else:
        lyrics = song.lyrics
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        lyrics = lyrics.replace('\n', ' ')
        lyrics = re.sub('\s{2,}', ' ', lyrics)
        if lyrics[0] == ' ':
            lyrics = lyrics[1:]
        
        extra_end_index = lyrics.rfind('EmbedShare')
        lyrics = lyrics[:extra_end_index]
        
        flag = True
        while flag:
            if len(lyrics) > 0:
                if lyrics[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    lyrics = lyrics[:-1]
                else:
                    flag = False
            else:
                flag = False

    return lyrics

# song, artist = clean_song_artist_names('By-Your-Side-(feat.-Tom-Grennan)', 'Calvin-Harris')
# lyrics = get_song_lyrics(song, artist)
# print(lyrics)

# with open('genius.csv', 'w', encoding='utf-8') as file:
#     file.write(str(lyrics))

df = pd.read_csv('data/data-test.csv')
df['lyrics'] = ''
for index, row in df.iterrows():
    artist = row['artist']
    song = row['track_name']
    song, artist = clean_song_artist_names(song, artist)
    lyrics = get_song_lyrics(song, artist)
    df.loc[index, 'lyrics'] = lyrics

df.to_csv('data/data-test-incl-lyrics.csv', index = False)