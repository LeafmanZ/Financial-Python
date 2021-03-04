import pandas as pd
import numpy as np
import datetime as dt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import easygui

infile = easygui.fileopenbox(msg="Please locate the csv file",
                             title = "Select a csv file")

sic_t = input("Enter the column title for industry SICs (ex. sic): ")
rev_t = input("Enter the column title for revenues (ex. revt): ")
n = int(float(input("Enter how many firms you want to calculate the concentration ratio: ")))
bins = int(float(input("Enter how many bins you want for the histograms:" )))

df = pd.read_csv(
    infile, 
    parse_dates = True, 
    index_col = 1, 
    na_values = ["", "C"]
)

sic_array = df[sic_t].to_numpy()
revt_array = df[rev_t].to_numpy()

sic_dict = {}
c_ratio_dict = {}
hhi_dict = {}

for sic in sic_array:
    sic_dict[sic] = []
    c_ratio_dict[sic] = 0
    hhi_dict[sic] = 0
    
for sic in sic_dict:
    for i in range(len(sic_array)):
        if sic_array[i] == sic:
            sic_dict[sic].append(revt_array[i])

for sic in sic_dict:
    if len(sic_dict[sic]) <= n:
        c_ratio_dict[sic] = 1
    else:
        c_ratio_dict[sic] = sum(sorted(sic_dict[sic],reverse = True)[:n])/sum(sic_dict[sic])
    
    hhi_dict[sic] = sum([(n*100/sum(sic_dict[sic]))**2 for n in sic_dict[sic]])
    
c_ratio_freq = [0] * bins
for i in range(bins):
    for ratio in c_ratio_dict.values():
        if ratio < (i+1)/bins and ratio > i/bins:
            c_ratio_freq[i] = c_ratio_freq[i]+1
            
c_ratio_bins = [0] * bins
for i in range(bins):
    c_ratio_bins[i] = "{:.0%}-{:.0%}".format(i/bins, (i+1)/bins)
    
hhi_freq = [0] * bins
for i in range(bins):
    for hhi in hhi_dict.values():
        if hhi < 10000*(i+1)/bins and hhi > 10000*i/bins:
            hhi_freq[i] = hhi_freq[i]+1

hhi_bins = [0] * bins
for i in range(bins):
    hhi_bins[i] = "{:.0f}-{:.0f}".format(10000*i/bins, 10000*(i+1)/bins)
    
fig = make_subplots(rows = 2, cols = 1, subplot_titles=( 
    "HHI Histogram", "Concentration Ratio Histogram"))

fig.add_bar(x = hhi_bins, y = hhi_freq, row=1, col=1)
fig.update_yaxes(title_text="Frequency of SICs", row=1, col=1)
fig.update_xaxes(title_text="HHI", row=1, col=1)

fig.add_bar(x = c_ratio_bins, y = c_ratio_freq, row=2, col=1)
fig.update_yaxes(title_text="Frequency of SICs", row=2, col=1)
fig.update_xaxes(title_text="Concentration Ratio", row=2, col=1)
fig.update_layout(
    height=1000, width=1000,
    title={
        'text': "Concentration Ratio and HHI by SIC",
        'y':.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    showlegend = False
)

fig.show()
fig.write_image("Industry Ratio Histograms.jpeg")
