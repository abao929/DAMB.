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
    total_colors = [('#000000','black'), ('#FFFFFF','white')]
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

def contour_plot(model, X_data, y_data, genres, xlabel, ylabel):
    h = 0.01
    x_min, x_max = X_data[:, 0].min() - 0.1, X_data[:, 0].max() + 0.1
    y_min, y_max = X_data[:, 1].min() - 0.1, X_data[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))
    

    indices = list(range(len(genres)))
    indices_dict = dict(zip(genres, indices))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = np.array([indices_dict[category] for category in Z])
    c = np.array([indices_dict[category] for category in y_data.to_numpy()])
    ZZ = Z.reshape(xx.shape)

    cmap = 'tab20'
    
    fig, ax = plt.subplots()
    ax.contourf(xx, yy, ZZ, cmap=cmap, alpha=0.7)
    scatter = ax.scatter(X_data[:, 0], X_data[:, 1], edgecolor='black', linewidth=0.2, alpha=0.7, c=c, cmap=cmap)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title('Model Clustering on danceability and loudness')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.legend(labels=list(indices_dict.keys()), handles=scatter.legend_elements()[0], bbox_to_anchor=(1, 1), loc='upper left')
    
    plt.show()

def main():
    train_data = pd.read_csv("../data/data-train-final.csv")
    train_data['color'] = 0
    
    for i in range(train_data['color'].size):
        rgb_val = (int(train_data['dominant-v'][i]), int(train_data['dominant-s'][i]), int(train_data['dominant-h'][i]))
        color_name = closest_colour(rgb_val)
        train_data['color'][i] = color_name
        #rgb_to_web(rgb_val)
    print(train_data['color'])

    # features = ['popularity','danceability','energy','key','loudness','valence','speechiness']
    features = ['valence','energy']

    relevant_features = features + ['color']
    train_data = train_data[relevant_features]
    dependent_variable = 'color'
    X = train_data[features].astype(float)
    y = train_data[dependent_variable]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
    knn, baseline = knn_and_baseline(X_train, y_train, X_val, y_val, train_data)

    if len(features) == 2:
        contour_plot(knn, X_train.to_numpy(), y_train, ['black', 'white'], features[0], features[1])



if __name__ == "__main__":
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    main()