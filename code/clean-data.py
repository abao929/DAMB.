import pandas as pd
import argparse
from scipy import stats
import numpy as np

def clean_data(df, output_path):
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


def remove_outliers(df, genre):
    features = ['popularity', 'danceability', 'energy',
                'key', 'loudness', 'modality', 'valence', 'speechiness']
    df = df[df['genre'] == genre]
    select_df = df[features]
    # print(df.shape)
    num_stds = 3
    z = np.abs(stats.zscore(select_df))
    # print(z)
    no_outliers = df[(z < num_stds).all(axis=1)]
    outliers = df[(z >= num_stds)]
    return no_outliers, outliers


def main():
    args = parse_args()
    # clean_data(args.d, args.o)
    df = pd.read_csv(args.d)
    print(df.shape)
    no_outliers, outliers = remove_outliers(df, 'pop')
    # print(no_outliers.shape, outliers.shape, outliers)
    cleaned_df = no_outliers

    genres = ['alternative', 'country', 'edm', 'jazz', 'classical', 'indie', 'metal', 'blues', 'kpop', 'r-n-b', 'hip-hop', 'rock', 'latin']
    for genre in genres:
        no_outliers, outliers = remove_outliers(df, genre)
        cleaned_df = cleaned_df.append(no_outliers)
    print(cleaned_df.shape)
    output_path = 'data/' + args.o
    cleaned_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()
