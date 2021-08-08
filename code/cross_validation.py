from sklearn.model_selection import cross_val_score



def main()
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

    selected_features = 'explicit-danceability-energy-key-speechiness'.split('-')
    X_df = X_df[selected_features]

    # Add polynomial features
    poly = preprocessing.PolynomialFeatures(2).fit(X_df)
    feature_names = poly.get_feature_names(X_df.columns)
    X_poly = poly.transform(X_df)
    X_df = pd.DataFrame(X_poly, columns=feature_names)


# Using the train_test_split function, create the train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_df, y_df, test_size=0.2, random_state=123)

    #Added Stuff for 
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_transformed = scaler.transform(X_train)
    clf = svm.SVC(C=1).fit(X_train_transformed, y_train)
    X_test_transformed = scaler.transform(X_test)
    clf.score(X_test_transformed, y_test)

    scores = cross_val_score(clf, X, y, cv=5)
    print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

if __name__ == "__main__":
    main()