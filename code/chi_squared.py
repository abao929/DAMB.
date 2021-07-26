import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import chi2_contingency
from colorutils import Color, rgb_to_web

import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
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

def main():
    train_data = pd.read_csv("../data/data-train-final.csv")
    train_data['color'] = 0
    
    for i in range(train_data['color'].size):
        rgb_val = (int(train_data['dominant-v'][i]), int(train_data['dominant-s'][i]), int(train_data['dominant-h'][i]))
        _, color_name = get_colour_name(rgb_val)
        train_data['color'][i] = color_name
        #rgb_to_web(rgb_val)
    print(train_data['color'])

    features = ['popularity','explicit','danceability','energy','key','loudness','modality','valence','speechiness']
    for feature in features:
        print('\nchi-sq test: color vs', feature)
        tstats, pval = chisquared_independence_test(train_data, 'color', feature)

if __name__ == "__main__":
    main()