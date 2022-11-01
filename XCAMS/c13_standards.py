import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyAstronomy import pyasl
import matplotlib.gridspec as gridspec

"""
Tuesday 1/11/2022 12:26

Here’s the C13 data – only those run on the dual inlet.
I’ve flagged bad data that can be ignored (in a separate tab).  I haven’t had a thorough look at the data, so there 
could be more bad data that should be flagged.  But good enough for now.
Some standards only have a single measurement, and many only have a couple of measurements (eg SIRI and GIRI samples).
I’d like to see how the 13C values scatter, as well as if there are any trends through time.  
Particularly we want to know if how we are doing in recent times – not sure if we want to look at just the last 1 year, 5 years, or something in between.

"""
"""Read in the data"""
df = pd.read_csv(r'H:\Science\Current_Projects\04_ams_data_quality\13C_standard_analysis_November2022\c13Standards2022_11_01.csv')
# for 1 year (begin 2022)
# df = df.loc[df['Job'] > 219966]
# # for 2 year (begin 2020)
# df = df.loc[df['Job'] > 214216]
# for 5 year (begin 2020)
df = df.loc[df['Job'] > 206292]

df = df.dropna(subset='SampleID')
df = df.dropna(subset='delta13C')
names = list((df['SampleID'].unique()))
#
"""Based on each unique sample ID, calculate summary information on each one"""
name = []
average = []
stddev = []
count = []

for i in range(0, len(names)):
    current_name = names[i]
    current_std = df.loc[df['SampleID'] == current_name]
    name.append(current_name)
    average.append(np.average(current_std['delta13C']))
    stddev.append(np.std(current_std['delta13C']))
    count.append(len(current_std))

    plt.scatter(current_std['Job'], current_std['delta13C'], label='{}'.format(current_name), color='black')
    plt.axhline((np.average(current_std['delta13C'])), color='black', alpha=0.15)
    plt.legend()
    plt.savefig('H:/Science/Current_Projects/04_ams_data_quality/13C_standard_analysis_November2022/plots/value{y}.png'.format(y=i), dpi=300, bbox_inches="tight")
    plt.close()
data = pd.DataFrame({"Sample ID": name, "Average": average, "1-sigma": stddev, "N": count}).sort_values("Sample ID",ascending=False).reset_index(drop=True)
"""Write that data to an excel sheet"""
data.to_excel('H:/Science/Current_Projects/04_ams_data_quality/C13_reduced.xlsx')

