import numpy as np
import pandas as pd


class Imputation:
    """
    Imputing missing values in a dataset.
    """
    def __init__(self, df):
        self.df = df

    def impute(self, method='mean'):
        ...
