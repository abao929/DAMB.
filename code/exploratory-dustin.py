import numpy as np
from numpy.core.numeric import indices
import pandas as pd
import random
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import seaborn as sns

RANDOM_SEED = 0

# Uses decision trees to determine feature importance; namely, 100 decision trees are created on
# subsets of the features and feature performance is determined on the tress' performances.
def decision_trees(X_train, y_train):
    trees = ExtraTreesClassifier(n_estimators=100)
    trees.fit(X_train, y_train)
    return trees

# Return the ANOVA f_scores of each feature
def f_scores(X_train, y_train):
	fs = SelectKBest(score_func=f_classif, k='all')
	fs.fit(X_train, y_train)
	return fs

def knn_and_baseline(X_train_, y_train_, X_test_, y_test_):
    knn = KNeighborsClassifier(n_neighbors=5)
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
    # Load the data from the bike-sharing.csv file into a Pandas DataFrame. Do not change
    # the variable name /data/
    # Hint: Look at the Pandas' read_csv function
    all_data = pd.read_csv('../data/data-train-final.csv')
    # print(all_data)

    # exclude = ['classical']
    exclude = []
    all_data = all_data[~all_data['genre'].isin(exclude)]

    # select only the relevant columns (features and dependent variable) that we will use
    relevant_cols = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness','genre','dominant-h','dominant-s','dominant-v']
    data = all_data[relevant_cols]

    # Uncomment this to print out the column names of data to know what features there are 
    # in the dataset
    # print("Columns: ", data.columns)
    
    features = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness','dominant-h','dominant-s','dominant-v']
    dependent_variable = 'genre'

    X = data[features].astype(float)
    y = data[dependent_variable]

    trees = decision_trees(X, y)
    feature_importances = trees.feature_importances_.tolist()
    print(feature_importances)
    # Uncomment this to display the bar graph of feature importances, according to the ensemble of decision trees
    plt.bar(features, feature_importances)
    plt.show()

    fs = f_scores(X, y)
    feature_f_scores = fs.scores_
    # Uncomment this to display the bar graph of f_scores for each feature
    plt.bar(features, feature_f_scores)
    plt.show()

    # Modify this to select the features use for classification
    selected_features = ['explicit', 'danceability','energy','loudness','speechiness']
    # selected_features = ['energy','loudness']
    # selected_features = ['explicit','speechiness']
    # selected_features = ['danceability','loudness']
    X_select = data[selected_features].astype(float)

    # Using the train_test_split function, create the train and validation sets.
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
    X_train_select = X_train[selected_features]
    X_val_select = X_val[selected_features]

    # Train the knn, determine the accuracy, and compare to the baseline
    knn, baseline = knn_and_baseline(X_train_select, y_train, X_val_select, y_val)

    # If we only use two features, we can create a scatter plot showing how the classifier divided the songs into categories
    if len(selected_features) == 2:
        h = 0.02
        X_data = X_train_select.to_numpy()
        x_min, x_max = X_data[:, 0].min() - 0.1, X_data[:, 0].max() + 0.1
        y_min, y_max = X_data[:, 1].min() - 0.1, X_data[:, 1].max() + 0.1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))
        
        genres = ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'heavy-metal', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative', 'blues', 'classical', 'country']
        for ex in exclude:
            genres.remove(ex)

        indices = list(range(len(genres)))
        indices_dict = dict(zip(genres, indices))
        
        Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = np.array([indices_dict[category] for category in Z])
        c = np.array([indices_dict[category] for category in y_train.to_numpy()])
        ZZ = Z.reshape(xx.shape)
        
        fig, ax = plt.subplots()
        cmap = plt.cm.get_cmap('tab20')
        ax.contourf(xx, yy, ZZ, cmap=cmap)
        scatter = ax.scatter(X_data[:, 0], X_data[:, 1], c=c, cmap=cmap, edgecolor='black', linewidth=0.2, alpha=0.7)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.title("15-Class classification")
        plt.xlabel(selected_features[0])
        plt.ylabel(selected_features[1])
        ax.legend(labels=list(indices_dict.keys()), handles=scatter.legend_elements(num=15)[0], bbox_to_anchor=(1, 1), loc='upper left')

        plt.show()

if __name__ == "__main__":
    main()