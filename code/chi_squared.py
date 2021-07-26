import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import chi2_contingency
from colorutils import Color

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

def main():
    train_data = pd.read_csv("../data/data-train-final.csv")
    train_data['color'] = 0
    
    for i in range(train_data['color'].size):
        rgb_val = (train_data['dominant-h'][i], train_data['dominant-s'][i], train_data['dominant-v'][i])
        train_data['color'][i] = Color(rgb=rgb_val).web

    tstats, pval = chisquared_independence_test(train_data, 'color', 'valence')

if __name__ == "__main__":
    main()