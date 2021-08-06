import pandas as pd
import argparse

def clean_data(path, output_path):
    df = pd.read_csv(path)
    print(df.shape)

    dup_features = ['album_id', 'album_name', 'cover_location',
                    'artist', 'track_id', 'track_name',
                    'popularity', 'explicit', 'danceability', 'energy',
                    'key', 'loudness', 'modality', 'valence',
                    'speechiness']
    df = df.drop_duplicates(subset = dup_features, keep=False)

    dup_features = ['artist', 'track_name', 'danceability', 'energy', 'key', 'loudness', 'modality', 'valence', 'speechiness']
    df = df.drop_duplicates(subset = dup_features)
    print(df.shape)

    dup_features = ['album_name', 'artist', 'track_name']
    df = df.drop_duplicates(subset = dup_features)
    print(df.shape)

    # dup_features = ['artist', 'track_name', 'modality', 'key', 'genre']
    # df = df.drop_duplicates(subset = dup_features)
    # print(df.shape)
    output_path = 'data/' + output_path
    df.to_csv(output_path, index=False)


def parse_args():
    parser = argparse.ArgumentParser(description='cleaning data')
    parser.add_argument('-d', help='path to data file', default='./../data/data-train-final-final.csv')
    parser.add_argument('-o', help='name of output file', default='clean-train.csv')
    return parser.parse_args()

def main():
    args = parse_args()
    clean_data(args.d, args.o)


if __name__ == '__main__':
    main()
