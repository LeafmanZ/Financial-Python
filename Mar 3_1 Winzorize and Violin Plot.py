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

df = pd.read_csv(
    'fang_example.csv', 
    parse_dates = True, 
    index_col = 1, 
    na_values = ["", "C"]
)
df.head()

df2 = pd.pivot_table(
    df,
    index = "date",
    columns = "TICKER",
    values = "RET")
df2.head()

mini = np.min(df2.min())
maxi = np.max(df2.max())

fig, (ax1, ax2) = plt.subplots(1,2)

sns.violinplot(data = df2, ax = ax1).set_title("Violinplot of returns\n not winsorized")

for col in df2.columns:
    df2[col]=mstats.winsorize(df2[col], limits=0.05)
    
sns.violinplot(data = df2, ax = ax2).set_title("Violinplot of returns\n winsorized")
ax1.set_ylim(mini,maxi)
ax2.set_ylim(mini,maxi)

plt.show()
