import pandas as pd
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

RANDOM_SEED = 0
N_NEIGHBORS = 5

def lin_reg(X_train, y_train, X_test, y_test):
    linear_regression = LinearRegression()
    linear_regression.fit(X_train, y_train)
    y_pred = linear_regression.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print('Linear Regression Mean squared error: ', mse)
    print('Coefficient of determination: ', r2)

    plt.scatter(X_test, y_test, color='red')
    plt.plot(X_test, y_pred, color='blue', linewidth=3)
    plt.show()

    return mse, r2

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
    print("Test statistics: ", tstats)
    print("p-value: ", pvalue)
    print("p-value < 0.05", pvalue < 0.05)

    # and then we'll return tstats and pvalue
    return tstats, pvalue

def knn_and_baseline(X_train_, y_train_, X_test_, y_test_):
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
    # select only the relevant columns (features and dependent variable) that we will use
    relevant_cols = ['key','valence', 'modality', 'dominant-s']
    train_data = train_data[relevant_cols]
    # train_data = train_data[feature_cols]

    features = ['valence', 'key']
    dependent_variable = 'modality'
    X = train_data[features].astype(float)
    y = train_data[dependent_variable].astype(float)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
    knn, baseline = knn_and_baseline(X_train, y_train, X_val, y_val)
    # oops linear regression doesn't really work in this context bc not continuous values
    # mse, r2 = lin_reg(X_train, y_train, X_val, y_val)
    # dependence between modality (major/minor) and valence (positivity)?
    tstats, pval = chisquared_independence_test(train_data, 'valence', 'modality')
    


if __name__ == "__main__":
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    main()