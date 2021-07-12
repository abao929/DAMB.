import random
import os
import csv

def tt_split(genre):
    '''
    Given a genre, randomly split all of the album covers in in data/genre by putting
    80% of the files in a train folder and the rest into a test folder.
    :param genre: the name of the genre to perform the split on 
    '''
    cur_folder = os.path.join('data', genre)
    album_covers = os.listdir(cur_folder)

    random.shuffle(album_covers)
    n_covers = len(album_covers)

    # The first 1/5th of the list of album covers is designated as test data,
    # while the rest of the list is designated as training data. By shuffling
    # the list of album covers beforehand, we ensure that our split is randomly
    # sampled.
    n_test = n_covers // 5
    test_covers = album_covers[:n_test]
    train_covers = album_covers[n_test:]

    # print(len(test_covers))
    # print(len(train_covers))

    os.makedirs(os.path.join('data', 'test', genre), exist_ok=True)
    os.makedirs(os.path.join('data', 'train', genre), exist_ok=True) 

    for cover in test_covers:
        os.rename(os.path.join(cur_folder, cover), os.path.join('data', 'test', genre, cover))
    for cover in train_covers:
        os.rename(os.path.join(cur_folder, cover), os.path.join('data', 'train', genre, cover))

def tt_split_csv(genre):
    '''
    Given a genre, append new rows to all-genres.csv, where each row
    contains information about a song in the playlist, including its
    album cover's new location after the train-test split.
    :param genre: the name of the genre to update the csv for
    '''
    file_name = genre + '.csv'
    new_rows = []

    # References the csv files created by collect-data.py
    with open(os.path.join('data', file_name), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            cover_path = row[4]
            new_row = row
            if os.path.isfile(os.path.join('data', 'test', cover_path)):
                new_row[4] = os.path.join('data', 'test', cover_path)
            else:
                new_row[4] = os.path.join('data', 'train', cover_path)
            new_rows.append(new_row)
    
    with open(os.path.join('data', 'all-genres.csv'), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

def main():
    # Clear the old csv file containing data on all of the images in the dataset, if one exists
    # This is done because the program appends to the csv file multiple times during a run 
    if os.path.exists(os.path.join('data', 'all-genres.csv')):
        open(os.path.join('data', 'all-genres.csv'), 'w').close()

    # For each genre, randomly split the images into an 80-20 train-test split,
    # and then update the csv file with the new images' locations
    for genre in ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'heavy-metal', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative', 'blues', 'classical', 'country']:
        tt_split(genre)
        tt_split_csv(genre)

if __name__ == '__main__':
    main()