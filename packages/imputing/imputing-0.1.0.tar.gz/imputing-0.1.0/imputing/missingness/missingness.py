import numpy as np
import pandas as pd


class Missingness:
    """
    Testing for type of missingness:
    Missing at Random (MAR), Missing Completely at Random (MCAR), Not Missing at Random
    """
    def __init__(self, df):
        self.df = df
