import os
import easygui
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd

# Get data from working directory
main_data = easygui.fileopenbox(msg= "Please locate the csv file",
                                title = "Select a csv file")

# Move data into dataframe
main_df = (pd.read_csv(main_data)).dropna()

# Preprocess returns
main_df = main_df[main_df.columns.to_numpy()[1:]].pct_change()
main_df = main_df.dropna()

# Run regression
results = sm.OLS(main_df['X.GSPC'], main_df['X.VIX']).fit()

# Save regression to text file
with open('Zieleman.txt', 'w') as fh:
    fh.write(results.summary().as_text()) 

# Make subplots
fig, axs = plt.subplots(2, 2, figsize=(20, 20))

# Make box plots
axs[0, 0].boxplot(main_df.drop(['X.VIX'], axis = 1), vert=True, patch_artist=True, labels=(main_df.drop(['X.VIX'], axis = 1)).columns.to_numpy()) 
axs[0, 0].set_title('Box Plot of Indices')
axs[0, 0].set(xlabel = 'Indices', ylabel = 'Returns')

# Make heat map
sn.heatmap(main_df.corr(), annot=True, ax = axs[0,1])
axs[0, 1].set_title('Correlogram of Indices')
axs[0, 1].set(xlabel = 'Indices', ylabel = 'Indices')

# Run regression for regression line and then plot regression on scatter plot
lr = sm.OLS(main_df['X.HSI'], sm.add_constant(main_df['X.GSPC'])).fit()
axs[1, 0].scatter(main_df['X.GSPC'], main_df['X.HSI'])
axs[1, 0].plot(main_df['X.GSPC'], lr.params[0] + lr.params[1]*main_df['X.GSPC'], 'r')
axs[1, 0].set_title('Relationship Between S&P and HSI')
axs[1, 0].set(xlabel = 'S&P returns', ylabel = 'HSI returns')

# Preprocess to calculate value of 1 dollar
main1_df = main_df.drop(columns=['X.VIX'])

# Make dict to hold dollar value cumulative returns
main_rets = {key: None for key in main1_df.columns}

# Calculate the normalized returns
for key in main_rets:
    tmp = 1
    main_ret = [tmp]
    for ret in main1_df[key]:
        tmp = tmp*1+ret  
        main_ret.append(tmp)
                  
    main_rets[key] = main_ret

# Plot the multiple normalized returns
for key in main_rets:
    axs[1, 1].plot(main1_df.index,(main_rets[key])[1:])

axs[1, 1].set_title('Value of $1 of Indices')
axs[1, 1].set(xlabel = 'Days', ylabel = 'Normalized Return')
axs[1, 1].legend(main1_df.columns)

fig.suptitle("Analysis of Indices Returns")

# Save subplot as jpg
fig.savefig(fname = 'Zieleman', format = 'jpg')                               
                     
