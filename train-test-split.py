import random
import os

def tt_split(folder_name):
    album_covers = os.listdir(folder_name)
    random.shuffle(album_covers)
    n_covers = len(album_covers)
    n_test = n_covers // 5 # 80:20 split
    test_covers = album_covers[:n_test]
    train_covers = album_covers[n_test:]

    # print(len(test_covers))
    # print(len(train_covers))

    os.makedirs(os.path.join('test', folder_name), exist_ok=True)
    os.makedirs(os.path.join('train', folder_name), exist_ok=True) 


    for cover in test_covers:
        os.rename(os.path.join(folder_name, cover), os.path.join('test', folder_name, cover))
    for cover in train_covers:
        os.rename(os.path.join(folder_name, cover), os.path.join('train', folder_name, cover))

        


def main():
    for folder_name in ['metal', 'pop', 'r-n-b', 'rock']:
        tt_split(folder_name)

if __name__ == '__main__':
    main()