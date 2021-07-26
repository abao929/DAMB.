import numpy as np
from numpy.core.numeric import indices
import pandas as pd
import random
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, Normalize
import math
from matplotlib.ticker import MultipleLocator

RANDOM_SEED = 0

# Uses decision trees to determine feature importance; namely, 100 decision trees are created on
# subsets of the features and feature performance is determined on the tress' performances.
def decision_trees(X_train, y_train):
    trees = RandomForestClassifier(n_estimators=100)
    trees.fit(X_train, y_train)
    return trees

# Return the ANOVA f_scores of each feature
def f_scores(X_train, y_train):
	fs = SelectKBest(score_func=f_classif, k='all')
	fs.fit(X_train, y_train)
	return fs

def model_and_baseline(X_train_, y_train_, X_test_, y_test_):
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train_, y_train_)
    model_score = model.score(X_test_, y_test_)
    print('Model mean accuracy for training set: ', model.score(X_train_, y_train_))
    print('Model mean accuracy for validation set: ', model_score)
    baseline1 = DummyClassifier(strategy='uniform')
    baseline1.fit(X_train_, y_train_)
    baseline1_score = baseline1.score(X_test_, y_test_)
    print('Baseline (random guessing) mean accuracy for validation set: ', baseline1_score)
    print('Model score is ', model_score / baseline1_score, ' times higher than baseline score')
    baseline2 = DummyClassifier(strategy='most_frequent')
    baseline2.fit(X_train_, y_train_)
    baseline2_score = baseline2.score(X_test_, y_test_)
    print('Baseline (guessing most frequent label) mean accuracy for validation set: ', baseline2_score)
    print('Model score is ', model_score / baseline2_score, ' times higher than baseline score')

    return model, baseline1, baseline2

# Draw a contour plot displaying how the model draws borders between classes
# Adapted from https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html#sphx-glr-auto-examples-neighbors-plot-classification-py
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
    ax.legend(labels=list(indices_dict.keys()), handles=scatter.legend_elements(num=len(genres))[0], bbox_to_anchor=(1, 1), loc='upper left')
    
    plt.show()

def main():
    # Load the data from the bike-sharing.csv file into a Pandas DataFrame. Do not change
    # the variable name /data/
    # Hint: Look at the Pandas' read_csv function
    all_data = pd.read_csv('../data/data-train-final.csv')
    # print(all_data)

    # exclude = []
    exclude = ['classical', 'country']
    # exclude = ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'heavy-metal', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative']
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
    # Normalize the features using min-max scaling
    min_max_scaler = preprocessing.MinMaxScaler()
    X_scaled = min_max_scaler.fit_transform(X.values)
    X = pd.DataFrame(X_scaled, columns=X.columns)

    y = data[dependent_variable]

    # Using the train_test_split function, create the train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)

    trees = decision_trees(X_train, y_train)
    print('Random forest train accuracy: %0.3f' % trees.score(X_train, y_train))
    print('Random forest val accuracy: %0.3f' % trees.score(X_val, y_val))
    feature_importances = permutation_importance(trees, X, y).importances_mean.tolist()
    # Uncomment this to display the bar graph of feature importances, according to the ensemble of decision trees
    plt.bar(features, feature_importances)
    plt.ylabel('Importance')
    plt.show()

    # fs = f_scores(X, y)
    # feature_f_scores = fs.scores_
    # # Uncomment this to display the bar graph of f_scores for each feature
    # plt.bar(features, feature_f_scores)
    # plt.show()

    # Modify this to select the features use for classification
    selected_features = ['popularity', 'danceability','energy','loudness','speechiness']
    # selected_features = ['energy','loudness']
    # selected_features = ['danceability','loudness']
    # selected_features = ['energy', 'danceability']
    # selected_features = ['loudness','speechiness']
    # selected_features = ['speechiness','loudness']
    # selected_features = ['dominant-h','dominant-s','dominant-v']
    # selected_features = ['dominant-h', 'dominant-v']    
    X_train_select = X_train[selected_features]
    X_val_select = X_val[selected_features]

    # Train the model, determine the accuracy, and compare to the baseline
    model, baseline1, baseline2 = model_and_baseline(X_train_select, y_train, X_val_select, y_val)

    y_pred = model.predict(X_val_select)
    y_true = []
    
    genres = ['metal', 'pop', 'r-n-b', 'rock', 'edm', 'heavy-metal', 'hip-hop', 'indie', 'jazz', 'kpop', 'latin', 'alternative', 'blues', 'classical', 'country']
    for ex in exclude:
        genres.remove(ex)
        
    indices = list(range(len(genres)))
    indices_dict = dict(zip(genres, indices))

    y_pred_indices = np.array([indices_dict[i] for i in y_pred])
    y_val_indices = np.array([indices_dict[i] for i in y_val])
    
    cm = confusion_matrix(y_val, y_pred, labels=genres)
    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm)
    plt.title('Confusion matrix of the classifier')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + genres)
    ax.set_yticklabels([''] + genres)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    # If we only use two features, we can create a scatter plot showing how the classifier divided the songs into categories
    if len(selected_features) == 2:
        
        contour_plot(model, X_train_select.to_numpy(), y_train, genres, selected_features[0], selected_features[1])

if __name__ == "__main__":
    main()