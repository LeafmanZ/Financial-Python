import pandas as pd
import numpy as np
import datetime as dt
import statistics as st
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import seaborn as sns
style.use('seaborn-dark-palette')

df = pd.read_csv(
    'fang_example.csv', 
    parse_dates = True, 
    index_col = 1, 
    na_values = ["", "C"]
)
df.head()

sns.boxplot(x="TICKER", y = "RET", data=df).set_title("Boxplot of returns")

import easygui

infile = easygui.fileopenbox(msg="Please locate the csv file",
                             title = "Select a csv file")

df = pd.read_csv(infile, parse_dates = True, index_col = 1, na_values=["","C"])
