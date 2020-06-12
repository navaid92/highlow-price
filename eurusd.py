# -*- coding: utf-8 -*-
"""EURUSD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uOZ9feptfSaSbCcV9TbTZcmMHvTw0zHx
"""

import numpy as np
import pandas as pd
import math
import sklearn
import sklearn.preprocessing
from sklearn.externals import joblib
import datetime
import os
import matplotlib.pyplot as plt

def Eurusdpredict(opens,low,high,close):
    valid_set_size_percentage = 10 
    test_set_size_percentage = 10
    
    df = pd.read_csv("EURUSD.csv", index_col = 0)
    df.head()

    df.info()

    df.describe()

    from sklearn import preprocessing, svm
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import math

    X=df[['Open','High','Low', "Close"]].values
    y=df[['Predicted High','Predicted Low']].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    clf = LinearRegression(n_jobs=-1)
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print(confidence)
    # now you can save it to a file
    joblib.dump(clf, 'eurusd.pkl') 
    # and later you can load it
    clf = joblib.load('eurusd.pkl')
    return clf.predict(np.array([[opens, low, high, close]]))
