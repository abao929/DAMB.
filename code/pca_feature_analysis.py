import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import feature_selection
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib
import matplotlib.cm as cm
import seaborn as sns
import random
import itertools
import os

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def model_and_baseline(X_train_, y_train_, X_test_, y_test_):
    # model = LogisticRegression()
    model = KNeighborsClassifier(n_neighbors=10)
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
    

def main():
    # pd.set_option("display.max_rows", None, "display.max_columns", None)

    all_data = pd.read_csv('../data/data-train-final-final.csv')

    genres = np.unique(all_data['genre'])
    exclude = ['heavy-metal']
    genres = np.setdiff1d(genres, exclude)
    all_data = all_data[~all_data['genre'].isin(exclude)].reset_index()
    print(all_data.genre.value_counts())
    exit()
    n_genres = genres.size
    relevant_cols = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness','genre','dominant-h','dominant-s','dominant-v']
    data = all_data[relevant_cols]
    # print(data.describe())

    # features = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness','dominant-h','dominant-s','dominant-v']
    features = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness']
    dependent_variable = 'genre'

    # Normalize the features using sklearn standard scaling
    X = data[features].astype(float)
    min_max_scaler = preprocessing.StandardScaler()
    X_scaled = min_max_scaler.fit_transform(X.values)
    X_df = pd.DataFrame(X_scaled, columns=X.columns)
    y_df = data[dependent_variable]

    graph_path = '../graphs'
    if not os.path.exists(graph_path):
        os.mkdir(graph_path)

    # for subset in findsubsets(features, 5):
    #     selected_features = list(subset)
    #     print(selected_features)
    #     print(len(selected_features))
    #     X_df_temp = X_df[selected_features]

    #     pca = PCA(n_components=3)
    #     X_reduced = pca.fit_transform(X_df_temp)
    #     data_reduced_df = pd.DataFrame(X_reduced, columns=['PCA feature 1', 'PCA feature 2', 'PCA feature 3'])
    #     data_reduced_df['Genre'] = y_df

    #     x = data_reduced_df['PCA feature 1']
    #     y = data_reduced_df['PCA feature 2']
    #     z = data_reduced_df['PCA feature 3']

    #     fig = plt.figure()
    #     ax = plt.axes(projection='3d')
    #     ax.set_xlabel("PCA feature 1")
    #     ax.set_ylabel("PCA feature 2")
    #     ax.set_zlabel("PCA feature 3")

    #     categories = np.unique(y_df)
    #     norm = matplotlib.colors.Normalize(vmin=0, vmax=n_genres - 1, clip=True)
    #     mapper = cm.ScalarMappable(norm=norm, cmap='tab20')

    #     for i, category in enumerate(categories):
    #         xi = [x[j] for j in range(len(x)) if y_df[j] == category]
    #         yi = [y[j] for j in range(len(x)) if y_df[j] == category]
    #         zi = [z[j] for j in range(len(x)) if y_df[j] == category]
    #         ax.scatter(xi, yi, zi, color=mapper.to_rgba(i), label=category)
    #     plt.legend(loc="lower right", bbox_to_anchor=(0.0, 0.0))

    #     plt.savefig('../graphs/' + '-'.join(selected_features) + '.png')
    #     plt.close()

    selected_features = 'explicit-danceability-energy-key-speechiness'.split('-')
    X_df = X_df[selected_features]

    # pca = PCA(n_components=3)
    # X_reduced = pca.fit_transform(X_df)
    # data_reduced_df = pd.DataFrame(X_reduced, columns=['PCA feature 1', 'PCA feature 2', 'PCA feature 3'])
    # data_reduced_df['Genre'] = y_df

    # x = data_reduced_df['PCA feature 1']
    # y = data_reduced_df['PCA feature 2']
    # z = data_reduced_df['PCA feature 3']

    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.set_xlabel("PCA feature 1")
    # ax.set_ylabel("PCA feature 2")
    # ax.set_zlabel("PCA feature 3")

    # categories = np.unique(y_df)
    # # print(categories)
    # norm = matplotlib.colors.Normalize(vmin=0, vmax=(n_genres), clip=True)
    # mapper = cm.ScalarMappable(norm=norm, cmap='tab20')

    # for i, category in enumerate(categories):
    #     xi = [x[j] for j in range(len(x)) if y_df[j] == category]
    #     yi = [y[j] for j in range(len(x)) if y_df[j] == category]
    #     zi = [z[j] for j in range(len(x)) if y_df[j] == category]
    #     ax.scatter(xi, yi, zi, color=mapper.to_rgba(i), label=category)
    # plt.legend(loc="lower right", bbox_to_anchor=(0.0, 0.0))

    # plt.show()
    # plt.clf()

    # Add polynomial features
    poly = preprocessing.PolynomialFeatures(2).fit(X_df)
    feature_names = poly.get_feature_names(X_df.columns)
    X_poly = poly.transform(X_df)
    X_df = pd.DataFrame(X_poly, columns=feature_names)

    # Using the train_test_split function, create the train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_df, y_df, test_size=0.2, random_state=123)
    model, baseline1, baseline2 = model_and_baseline(X_train, y_train, X_val, y_val)
    y_pred = model.predict(X_val)        
    indices = list(range(len(list(genres))))
    indices_dict = dict(zip(list(genres), indices))

    y_pred_indices = np.array([indices_dict[i] for i in y_pred])
    y_val_indices = np.array([indices_dict[i] for i in y_val])
    
    conf_mat = confusion_matrix(y_val, y_pred, labels=list(genres))
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    cax = ax.matshow(conf_mat)
    plt.title('Confusion matrix of the classifier')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + list(genres))
    ax.set_yticklabels([''] + list(genres))
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

if __name__ == "__main__":
    main()