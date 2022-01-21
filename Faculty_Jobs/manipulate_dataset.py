# manipulate_dataset.py

"""This module provides functionalities to manipulate data gathered from scraping"""

import pandas as pd


def read_datasets():
    loc_dataset = pd.read_csv("jobs_by_loc.tsv",
                              names=["Title", "Posted On", "Page Link"],
                              sep="\t", encoding="UTF-8"
                              )
    category_dataset = pd.read_csv("jobs_by_category.tsv",
                                   names=["Title", "Posted On", "Page Link"],
                                   sep="\t", encoding="UTF-8"
                                   )
    return pd.concat([loc_dataset, category_dataset], ignore_index=True)


def find_intersection(df):
    filter1 = df["Title"].duplicated()
    return df.loc[filter1, :]


def find_uniques(df):
    filter1 = df["Title"].duplicated()
    return df.loc[~filter1, :]


if __name__ == "__main__":
    df1 = read_datasets()
    filtered_results = find_uniques(df1)
