import pandas as pd

def transform_bmi(X):
    bins = [0, 29.999, 100]
    labels = ['Normal weight', 'Obesity']
    X = X.copy()
    X["bmi_category"] = pd.cut(X['bmi'], bins=bins, labels=labels, right=False)
    return X

def bmi_calculation(size, weight):
    convert_weight = weight / 100
    return round((convert_weight / size**2),2)

