# Data Deliverable Report - DAMB.

**Team members**: Dustin Wu, Alex Bao, Matthew Lee, and Beatrice Hoang **[edit this]**

## Step 1

1. We first queried Spotify's API to determine what genres of songs Spotify defines, and then selected 15 genres that we felt were distinct and popular enough to classify. We searched Spotify for Spotify-generated and user-generated playlists pertaining to a specific genre (e.g. a pop music playlist or a metal music playlist), and saved the Spotify ids of these playlists. We then made requests to Spotify's API to get the songs of the playlist, and then for each song we extracted the url of the song's album cover. We then downloaded the album cover at this url and placed it in a directory corresponding to the genre of the playlist. In addition, we saved metadata relating to each cover that we collected, such as the name of the album and the name of the artist(s) in a csv file for each genre. 

2. Our data partially consists of user-created playlists, so part of our data relies on the classifications of Spotify users. However, we believe that these classifications are reputable, because 1) we selected highly popular playlists, so the playlists we selected have the backing of many users on the site who approve of the song choices and 2) the classification of genres as a whole has a lot to do with how listeners recognize specific  traits in a song, and so user-generated playlists satisfy our goal of classifying genres. 

At first we had planned on getting genre labels from Spotify's API, since the documentation does list a genre attribute as a return value for the documentation. However, we found that the vast majority of songs were not labelled with a genre, so all we got was an empty string. Therefore, we decided that relying on playlists to obtain labels would both yield fairly accurate labels without having to spend siginifant labor on manually labelling each song.

## Step 2

The 

## Step 3

1. Your observation of the data prior to cleaning the data goes here (limit: 250 words)
2. Your data cleaning process and outcome goes here (at most around 250 words)

## Step 4

Your train-test data descriptions goes here (at most around 250 words)

## Step 5

Your socio-historical context & impact report goes here

## Step 6

Your team report goes here