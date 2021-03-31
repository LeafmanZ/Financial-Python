import pandas as pd
import numpy as np
import datetime as dt
import statistics as st
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import seaborn as sns
style.use('seaborn-dark-palette')
from scipy.stats import mstats
from matplotlib import ticker as mtick
from scipy import stats

df = pd.read_csv(
    'fang_example.csv', 
    parse_dates = True, 
    index_col = 1, 
    na_values = ["","C"]
)
df.head()

fig, (ax1,ax2,ax3) = plt.subplots(3,1)

sns.boxplot(x = "TICKER", y = "RET", data =df, ax= ax1).set_title("Boxplot of returns")

sns.histplot(df, x = "RET", hue="TICKER", edgecolor = "grey", stat = "density", alpha = .3, common_norm = False,
            ax = ax2).set(title='Histogram of stock returns')
            
sns.violinplot(x = "TICKER", y = "RET", data = df, ax = ax3).set_title("Violinplot of returns")
plt.subplots_adjust(hspace = .5)
plt.show()
