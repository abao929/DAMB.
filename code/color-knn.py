import pandas as pd
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

import seaborn as sns
from matplotlib.colors import ListedColormap
# from colorutils import Color, rgb_to_hex

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

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def chisquared_independence_test(df, column_a_name, column_b_name):
    """
    Input:
        - df: a Pandas DataFrame
        - column_a_name: str, a name of a feature in the table df
        - column_b_name: str, a name of another feature in the table df
    Output:
        - tstats: a float, describing the test statistics
        - p-value: describing the p-value of the test
    """
    # Create a cross table between the two columns a and b
    cross_table = pd.crosstab(df[column_a_name], df[column_b_name])

    # Use scipy's chi2_contingency
    # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)
    # to get the test statistic and the p-value
    tstats, pvalue, _, _ = chi2_contingency(cross_table)

    ## TODO: You can uncomment to print out the test statistics and pvalue to 
    ## determine your answer to the questions
    print("Test statistic: ", tstats)
    print("p-value: ", pvalue)
    print("p-value < 0.05", pvalue < 0.05)

    # and then we'll return tstats and pvalue
    return tstats, pvalue

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

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Create color maps
    # cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA','#00AAFF'])
    # cmap_bold = ListedColormap(['#FF0000', '#00FF00','#00AAFF'])

    # h = .02
    # x_min, x_max = X_train_.iloc[:, 0].min() - 1, X_train_.iloc[:, 0].max() + 1
    # y_min, y_max = X_train_.iloc[:, 1].min() - 1, X_train_.iloc[:, 1].max() + 1
    # xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
    # np.arange(y_min, y_max, h))

    # # predict class using data and kNN classifier
    # Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])

    # # Put the result into a color plot
    # Z = Z.reshape(xx.shape)
    # plt.figure()
    # plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # # Plot also the training points
    # plt.scatter(X_train_.iloc[:, 0], X_train_.iloc[:, 1], c=y_train_, cmap=cmap_bold)
    # plt.xlim(xx.min(), xx.max())
    # plt.ylim(yy.min(), yy.max())
    # plt.title("3-Class classification (k = %i)" % (5))
    # plt.show()
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

    # features = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness']
    # for feature in features:
    #     print('\nchi-sq test: color vs', feature)
    #     tstats, pval = chisquared_independence_test(train_data, 'color', feature)
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