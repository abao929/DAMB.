from sklearn.cluster import KMeans
import cv2
from collections import Counter
import os
import csv

def get_dominant_color(image, k=4, image_processing_size = None):
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size, 
                            interpolation = cv2.INTER_AREA)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)
    label_counts = Counter(labels)
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
    return list(dominant_color)

def get_dominant_colors_from_csv(csv_name):
    new_rows = []
    with open(csv_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:

            file_path = row[2]
            file_path_parts = file_path.split(os.path.sep)

            train_path = os.path.join(file_path_parts[0], 'train', file_path_parts[1], file_path_parts[2])
            test_path = os.path.join(file_path_parts[0], 'test', file_path_parts[1], file_path_parts[2])

            img = None

            if os.path.isfile(train_path):
                img = cv2.imread(train_path)
            elif os.path.isfile(test_path):
                img = cv2.imread(test_path)
            else:
                continue

            dominant_color = get_dominant_color(img)
            row += dominant_color
            new_rows.append(row)
            
    return new_rows

def augment_csv(csv_name, new_rows):
    with open(csv_name[:-4] + '-plus-color.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['album_id', 'album_name', 'cover_location', 'artist', 'track_id', 'track_name', 'popularity', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'modality', 'energy', 'valence', 'speechiness', 'genre', 'dominant-h', 'dominant-s', 'dominant-v'])
        writer.writerows(new_rows)
    
new_data_train = get_dominant_colors_from_csv(os.path.join('data', 'data-train.csv'))
new_data_test = get_dominant_colors_from_csv(os.path.join('data', 'data-test.csv'))

augment_csv(os.path.join('data', 'data-train.csv'), new_data_train)
augment_csv(os.path.join('data', 'data-test.csv'), new_data_test)