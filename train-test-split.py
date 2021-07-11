import random
import os
import csv

def tt_split(genre):
    cur_folder = os.path.join('data', genre)
    album_covers = os.listdir(cur_folder)
    random.shuffle(album_covers)
    n_covers = len(album_covers)
    n_test = n_covers // 5 # 80:20 split
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
    file_name = genre + '.csv'
    test_rows = []
    train_rows = []

    with open(os.path.join('data', file_name), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            # print(row)
            cover_path = row[4]
            if os.path.isfile(os.path.join('test', cover_path)):
                test_rows.append(row)
            else:
                train_rows.append(row)
    
    with open(os.path.join('data', 'test', genre + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(['name', 'artist', 'cover_url', 'album_url', 'album_path'])
        writer.writerows(test_rows)

    with open(os.path.join('data', 'train', genre + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(['name', 'artist', 'cover_url', 'album_url', 'album_path'])
        writer.writerows(train_rows)

def main():
    for genre in ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'heavy-metal', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative', 'blues', 'classical', 'country']:
        tt_split(genre)
        tt_split_csv(genre)

if __name__ == '__main__':
    main()