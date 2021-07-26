import pandas as pd
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

import webcolors

N_NEIGHBORS = 5
RANDOM_SEED = 0

def closest_colour(requested_colour):
    min_colours = {}
    total_colors = [('#FF0000','red'), ('#FFA500','orange'), ('#FFFF00','yellow'),
                    ('#008000','green'), ('#0000FF','blue'), ('#800080','purple'),
                    ('#000000','black'), ('#FFFFFF','white'), ('#582705','brown')]
    for key, name in total_colors: #webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def knn_and_baseline(X_train_, y_train_, X_test_, y_test_, dataset):
    knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS)
    knn.fit(X_train_, y_train_)
    knn_score = knn.score(X_test_, y_test_)
    print('KNN mean accuracy for validation set: ', knn_score)
    baseline = DummyClassifier(strategy='uniform')
    baseline.fit(X_train_, y_train_)
    baseline_score = baseline.score(X_test_, y_test_)
    print('Baseline (random guessing) mean accuracy for validation set: ', baseline_score)
    print('KNN score is ', knn_score / baseline_score, ' times higher than baseline score')

    return knn, baseline


def main():
    train_data = pd.read_csv("../data/data-train-final.csv")
    train_data['color'] = 0
    
    for i in range(train_data['color'].size):
        rgb_val = (int(train_data['dominant-v'][i]), int(train_data['dominant-s'][i]), int(train_data['dominant-h'][i]))
        color_name = closest_colour(rgb_val)
        train_data['color'][i] = color_name
        #rgb_to_web(rgb_val)
    print(train_data['color'])

    features = ['popularity','danceability','energy','key','loudness','valence','speechiness']
    relevant_features = features + ['color']
    train_data = train_data[relevant_features]
    dependent_variable = 'color'
    X = train_data[features].astype(float)
    y = train_data[dependent_variable]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
    knn, baseline = knn_and_baseline(X_train, y_train, X_val, y_val, train_data)

if __name__ == "__main__":
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    main()