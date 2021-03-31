import os
import easygui
import numpy as np
from scipy.stats import mstats
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Get data from a directory
main_data = easygui.fileopenbox(msg="Please locate the csv file", title = "Select a csv file")

num_bins = int(input("Enter the number of bins you want to use for a histogram: "))
print("\n")
print("Please wait. Loading Data...")

# Move data into dataframe

headers = ['Enterprise Flag', 'Record Number', 'US Postal State Code', 'Metropolitan Statistical Area (MSA) Code', 
 'County - 2010 Census', 'Census Tract - 2010 Census', '2010 Census Tract - Percent Minority',
 '2010 Census Tract - Median Income', 'Local Area Median Income', 'Tract Income Ratio', 
 'Borrower’s Annual Income', 'Area Median Family Income (2019)', 'Borrower Income Ratio',
 'Acquisition Unpaid Principal Balance (UPB)', 'Purpose of Loan', 'Federal Guarantee', 'Number of Borrowers',
 'First-Time Home Buyer', 'Borrower Race 1', 'Borrower Race 2', 'Borrower Race 3', 'Borrower Race 4',
 'Borrower Race 5', 'Borrower Ethnicity', 
 'Co-Borrower Race 1', 'Co-Borrower Race 2', 'Co-Borrower Race 3', 'Co-Borrower Race 4', 'Co-Borrower Race 5', 
 'Co-Borrower Ethnicity',
 'Borrower Gender', 'Co-Borrower Gender', 'Age of Borrower', 'Age of Co-Borrower', 'Occupancy Code', 'Rate Spread',
 'HOEPA Status', 'Property Type', 'Lien Status', 'Borrower Age 62 or older', 'Co-Borrower Age 62 or older',
 'Loan-to-Value Ratio (LTV) at Origination', 'Date of Mortgage Note', 'Term of Mortgage at Origination',
 'Number of Units', 'Interest Rate at Origination', 'Note Amount', 'Preapproval', 'Application Channel', 
 'Automated Underwriting System (AUS) Name', 'Credit Score Model - Borrower', 'Credit Score Model - Co-Borrower',
 'Debt-to-Income (DTI) Ratio', 'Discount Points', 'Introductory Rate Period', 
 'Manufactured Home – Land Property Interest', 'Property Value', 'Rural Census Tract',
 'Lower Mississippi Delta County', 'Middle Appalachia County', 'Persistent Poverty County',
 'Area of Concentrated Poverty', 'High Opportunity Area', 'Qualified Opportunity Zone (QOZ) Census Tract']

main_df = pd.read_csv(main_data, sep = "\s+", header=None)
main_df.columns = headers

selection = ['Local Area Median Income', 'Borrower’s Annual Income', 'First-Time Home Buyer',
             'Borrower Gender', 'Age of Borrower', 'Property Value']
total_data_df = main_df[selection]

print("Please wait. Transforming Data...")
# Clean data
data_df = total_data_df.copy()
data_df = data_df.loc[data_df['Local Area Median Income']!=999999]
data_df = data_df.loc[data_df['Borrower’s Annual Income']!=999999998]
data_df = data_df.loc[data_df['First-Time Home Buyer']!=9]
data_df = data_df.loc[data_df['Borrower Gender']!=9]
data_df = data_df.loc[data_df['Borrower Gender']!=4]
data_df = data_df.loc[data_df['Borrower Gender']!=3]
data_df = data_df.loc[data_df['Age of Borrower']!=9]
data_df = data_df.loc[data_df['Property Value']!=999999999]

explanatory_vars = ['Local Area Median Income', 'Borrower’s Annual Income', 'Property Value']
dependent_vars = ['First-Time Home Buyer', 'Borrower Gender', 'Age of Borrower']

data_df.loc[data_df['First-Time Home Buyer'] == 1, 'First-Time Home Buyer'] = 'Yes'
data_df.loc[data_df['First-Time Home Buyer'] == 2, 'First-Time Home Buyer'] = 'No'

data_df.loc[data_df['Borrower Gender'] == 1, 'Borrower Gender'] = 'Male'
data_df.loc[data_df['Borrower Gender'] == 2, 'Borrower Gender'] = 'Female'

data_df.loc[data_df['Age of Borrower'] == 1, 'Age of Borrower'] = '0-25'
data_df.loc[data_df['Age of Borrower'] == 2, 'Age of Borrower'] = '25-34'
data_df.loc[data_df['Age of Borrower'] == 3, 'Age of Borrower'] = '35-44'
data_df.loc[data_df['Age of Borrower'] == 4, 'Age of Borrower'] = '45-54'
data_df.loc[data_df['Age of Borrower'] == 5, 'Age of Borrower'] = '55-64'
data_df.loc[data_df['Age of Borrower'] == 6, 'Age of Borrower'] = '65-74'
data_df.loc[data_df['Age of Borrower'] == 7, 'Age of Borrower'] = '74+'

print("Please wait. Analyzing Data...")

data_dict = {}
for e_var in explanatory_vars:
    
    metric_dict = {}
    for d_var in dependent_vars:

        # get unique values of category
        metric = []
        x = data_df[d_var].unique()
        x.sort()
        for i in range(len(x)):
            val = x[i]
            # get average values of each explanatory variable by category
            metric.append(((data_df.loc[data_df[d_var]==val])[e_var]).mean(axis=0))
        
        metric_list = [metric, x]
        metric_dict[d_var] = metric_list
    
    winz_data =mstats.winsorize(data_df[e_var], limits=0.05)
    max_val = max(winz_data)
    bin_arr = [0]
    for n in range(num_bins):
        bin_arr.append((n+1)/num_bins * max_val)
        
    hist = np.histogram(winz_data, bins = bin_arr)
    new_hist_x_axis = []
    hist_d_var = hist[1]
    for i in range(len(hist_d_var)-1):
        bin_str = "{}k-{}k".format(int(hist_d_var[i]/1000), int(hist_d_var[i + 1]/1000))
        new_hist_x_axis.append(bin_str)

    metric_dict['Histogram'] = [hist[0],new_hist_x_axis]  
    avg_str = 'Average ' + e_var
    data_dict[avg_str] = metric_dict
    
    e_var = explanatory_vars[-1]

metric_dict = {}
for d_var in dependent_vars:
    
    # get unique values of category
    metric = []
    x = data_df[d_var].unique()
    x.sort()
    for i in range(len(x)):
        val = x[i]
        # get average values of each explanatory variable by category val
        metric.append(((data_df.loc[data_df[d_var]==val])[e_var]).sum(axis=0))
        
    metric_list = [metric, x]
    metric_dict[d_var] = metric_list

winz_data =mstats.winsorize(data_df[e_var], limits=0.05)
max_val = max(winz_data)
bin_arr = [0]
for n in range(num_bins):
    bin_arr.append((n+1)/num_bins * max_val)

hist = np.histogram(winz_data, bins = bin_arr)
new_hist_x_axis = []
hist_d_var = hist[1]
for i in range(len(hist_d_var)-1):
    bin_str = "{}k-{}k".format(int(hist_d_var[i]/1000), int(hist_d_var[i + 1]/1000))
    new_hist_x_axis.append(bin_str)

metric_dict['Histogram'] = [hist[0],new_hist_x_axis]           
avg_str = 'Total ' + e_var
data_dict[avg_str] = metric_dict

ddk = list(data_dict.keys())

keep_ask = True
while keep_ask:
    print('\n')
    input_str = "Select the number of the metric you want to view \n 1: {} \n 2: {} \n 3: {} \n 4: {}\n".format(ddk[0],ddk[1],ddk[2],ddk[3])

    selected_num = int(input(input_str))
    print('\n')

    Selected_Metric = ddk[selected_num - 1]
    metric_dict = data_dict[Selected_Metric]
    
    mdk = list(metric_dict.keys())
    title_str1 = '{} by {}'.format(Selected_Metric, dependent_vars[0])
    title_str2 = '{} by {}'.format(Selected_Metric, dependent_vars[1])
    title_str3 = '{} by {}'.format(Selected_Metric, dependent_vars[2])
    title_str4 = 'Histogram of all {}'.format((Selected_Metric.replace('Average ','')).replace('Total ',''))

    fig = make_subplots(rows = len(mdk)//2, cols = 2,
                        vertical_spacing = .8/4, horizontal_spacing = .4/2,
                        subplot_titles = (title_str1, title_str3, title_str2, title_str4))
    color_schemes = ['steelblue', 'firebrick', 'darkmagenta', 'darkgoldenrod']

    color_count = 0
    for i in range(len(mdk)):

        r = i + 1
        c = 1
        if i >= len(mdk)//2:
            r = i - len(mdk)//2 + 1
            c = 2

        key = mdk[i]

        X = (metric_dict[key])[1]
        Y = (metric_dict[key])[0]

        lower = min(Y)*.95
        upper = max(Y)*1.01

        fig.add_trace(go.Bar(x= X, y= Y),r,c)
        fig.update_xaxes(title_font_size =12, title_text=key, row=r, col=c)
        fig.update_yaxes(title_font_size =12,
                         title_text='{} ($)'.format((Selected_Metric.replace('Average ','')).replace('Total ',''))
                         , range = [lower, upper], row=r, col=c)

        fig.update_traces(marker_color= color_schemes[color_count],row=r, col=c)
        color_count = color_count + 1

        if i == 3:
            fig.update_xaxes(title_text='{} ($)'.format((Selected_Metric.replace('Average ','')).replace('Total ','')), row=r, col=c)
            fig.update_yaxes(tickformat=None,title_text='Frequency', row=r, col=c)

    fig.update_layout(
        height=800, width=1200,
        title={
            'text': Selected_Metric + ' by Demographic',
            'y':.97,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font_size = 20,
        showlegend = False
    )

    fig.show()
    
    again_str = input("Do you want another metric (Yes or No)?: " )
    
    if again_str.upper() != "YES":
        keep_ask = False
