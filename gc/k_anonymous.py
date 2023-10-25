import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def isKAnonymized(df, k):
    for index, row in df.iterrows():
        query = ' & '.join([f'{col} == {row[col]}' for col in df.columns])
        rows = df.query(query)
        if rows < k:
            return False
    return True
