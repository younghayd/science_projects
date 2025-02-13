"""
This file originally existed in SOAR Tree Rings folder but was moved when it was decided that this small work could
be publishable.

We want to align oceanographic D14C measurements with water-masses. The idea came about because I wanted to see
what canonical "ages" certain water masses have in the Southern Ocean, and such a database didn't exist. So here I'm
going to create it.
"""
import pandas.errors

"""
For the discussion section of my paper, I want to see where D14C values are and where they occur in reference to specific
water masses; however, such a database doesn't exist. So I'll create it; and publish it.
"""

from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import patoolib
import matplotlib.pyplot as plt
import warnings


#
# warnings.filterwarnings("ignore")
"""
# wmc for water mass characteristics from Emery:
# https://curry.eas.gatech.edu/Courses/5225/ency/Chapter11/Ency_Oceans/Water_Types_Masses.pdf
When speaking to Joellen Russel at NIWA, she said I should look for Lynne Talley's inverse modeling paper
where she assigns water masses to T and S values. THIS is the data I should use to assign my water masses. 
"""
# TODO get water mass characteristics file from Talley! Joellen Russel said she's respond to you when shes back from leave
# TODO If not, ask Lynne herself.

wmc = pd.read_csv(f'H:\Science\Datasets\Water_Mass_Characteristics.csv', skiprows=2, comment='#')


"""
I've bulk downloaded all the GOSHIP files, see directory on line below. 
"""
results_names = []
res_2 = []
onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\Bulk_Download') if isfile(join(r'H:\Science\Datasets\Hydrographic\Bulk_Download', f))]


database = pd.DataFrame()
for i in range(0, len(onlyfiles)):
    try:
        print(f'loop 1: {i/len(onlyfiles)}')
        # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
        data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\Bulk_Download\{onlyfiles[i]}', skiprows=2, comment='#')
        database = pd.concat([database, data])
        results_names.append(str(onlyfiles[i]))
        res_2.append("Successfully Read")

    except UnicodeDecodeError:
        results_names.append(str(onlyfiles[i]))
        res_2.append("Not read: UnicodeDecodeError")

"""
Now I'm adding on GLODAP data, see scrape_GLODAP.py
"""

onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2') if isfile(join(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2', f))]

for i in range(0, len(onlyfiles)):
    try:
        print(f'loop 1: {i/len(onlyfiles)}')
        # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
        data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\GLODAP_scrape2\{onlyfiles[i]}', skiprows=2, comment='#')
        database = pd.concat([database, data])
        results_names.append(str(onlyfiles[i]))
        res_2.append("Successfully Read")

    except UnicodeDecodeError:
        results_names.append(str(onlyfiles[i]))
        res_2.append("Not read: UnicodeDecodeError")
    except pandas.errors.ParserError:
        results_names.append(str(onlyfiles[i]))
        res_2.append("Not read: PandasParserError")

database = database.dropna(subset='DELC14')
database = database.dropna(subset='LONGITUDE')
results = pd.DataFrame({"Filename":results_names, "Result": res_2})

with pd.ExcelWriter(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.csv', mode='a') as writer:
    database.to_excel(writer, sheet_name='Database')
    results.to_excel(writer, sheet_name='FileErrors')




# See Full list of column names
# print(database.columns.tolist())

# I ONLY CARE ABOUT 14C!!!
#
#
# ocean_array = []
# # Need to assign ocean-sector labels to the data: Pacific, Atlantic, or Indian. Southern not included in WMC, looped into each 3.
# # for i in range(0, len(database)):
# for i in range(0, len(database)):
#     row = database.iloc[i]
#     x = row['LONGITUDE']
#
#     if type(x) == str:
#         ocean_array.append('Type Error: Lon = String')
#
#     elif 30 < float(row['LONGITUDE']) < 150:
#         ocean_array.append('Indian')
#     elif 50 < float(row['LONGITUDE']) < 180:
#         ocean_array.append('Pacific')
#     elif -180 < float(row['LONGITUDE']) < -60:
#         ocean_array.append('Pacific')
#     elif -60 < float(row['LONGITUDE']) < 0:
#         ocean_array.append('Atlantic')
#     elif 0 < float(row['LONGITUDE']) < 30:
#         ocean_array.append('Atlantic')
#     else:
#         ocean_array.append('Outside Boundaries')
#
# database['Ocean_Label'] = ocean_array
# # test = database.loc[database['Ocean_Label'] == 'Type Error: Lon = String']
# # print(len(test))
# # print(len(database))
# # About 10% of all the data got flagged as bad beacuse the lon couldn't be converted to strings. These
# # Usually showed up as just empty cells but weren't dropped by nan. there's likely a spacebar that was hit in these places.
#
# database = database.loc[database['Ocean_Label'] != 'Type Error: Lon = String']
#
#
# water_masses = []
# # Now I want to assign water masses based on the data in "WMC"
# for i in range(0, len(database)):
#     # grab the first row
#     row = database.iloc[i]
#
#     # set an escape label to avoid double labeling
#     escapeflag = 'N'
#
#     for k in range(0, len(wmc)):
#         # grab the first row of water mass characteristics
#         wmc_row = wmc.iloc[k]
#         name = wmc_row['Name']
#
# # including depth filtering
#         # if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDPRS MIN']) < float(row['CTDPRS']) < float(wmc_row['CTDPRS MAX']) and float(wmc_row['CTDTMP MIN']) < float(row['CTDTMP']) < float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) < float(row['CTDSAL']) < float(wmc_row['SALNTY MAX']):
#         #     water_masses.append(name)
#         #     escapeflag = 'Y'
#         #     break
#  # not including CTDPRS filter
#         if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDTMP MIN']) < float(row['CTDTMP']) < float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) < float(row['CTDSAL']) < float(wmc_row['SALNTY MAX']):
#             water_masses.append(name)
#             escapeflag = 'Y'
#             break
#
#     if escapeflag == 'N':  # I still haven't found a match
#         water_masses.append('Error: No Water Mass Assigned')
#
# database['Water Mass'] = water_masses
# database.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_full.csv')
#


# """
# UNCOMMENT ABOVE IF YOU NEED TO EDIT OR REBUILD THE DATABASE. CONTINUE DOWN IF YOU WANT PLOTS
# """
#
#
# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_full.csv')
# df = df.loc[df['DELC14'] > -999]
# df = df.loc[df['SALNTY'] > -999]
# df = df.loc[df['Water Mass'] != 'Error: No Water Mass Assigned']
# df.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_cleaned.csv')
#
# df = df.dropna(subset='DELC14')
#
# pacific = df.loc[df['Ocean_Label'] == 'Pacific']
# names = np.unique(pacific['Water Mass'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass'] == names[i]]
#
#     fig = plt.figure(figsize=(12,6))
#     gs = gridspec.GridSpec(2, 4)
#     gs.update(wspace=.6, hspace=.6)
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#     plt.scatter(this_wm['LATITUDE'], this_wm['CTDPRS'], c=this_wm['DELC14'], cmap='magma')
#     plt.ylim(4000, 0)
#     plt.xlim(-70, 70)
#     plt.title(f"Pacific -  {str(names[i])}")
#     plt.ylabel('Depth (CTD Pressure)')
#     plt.xlabel('Latitude')
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
#     plt.scatter(this_wm['SALNTY'], this_wm['CTDTMP'], c=this_wm['DELC14'], cmap='magma')
#     plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270)
#     plt.title(f"Pacific -  {str(names[i])}")
#     plt.ylabel('CTD Temperature')
#     plt.xlabel('Salinity (PSU)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/WaterMasses/Pacific_Ocean_{names[i]}.png')
#     plt.close()
#
#
# pacific = df.loc[df['Ocean_Label'] == 'Indian']
# names = np.unique(pacific['Water Mass'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass'] == names[i]]
#
#     fig = plt.figure(figsize=(12,6))
#     gs = gridspec.GridSpec(2, 4)
#     gs.update(wspace=.6, hspace=.6)
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#     plt.scatter(this_wm['LATITUDE'], this_wm['CTDPRS'], c=this_wm['DELC14'], cmap='magma')
#     plt.ylim(4000, 0)
#     plt.xlim(-70, 70)
#     plt.title(f"Indian -  {str(names[i])}")
#     plt.ylabel('Depth (CTD Pressure)')
#     plt.xlabel('Latitude')
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
#     plt.scatter(this_wm['SALNTY'], this_wm['CTDTMP'], c=this_wm['DELC14'], cmap='magma')
#     plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270)
#     plt.title(f"Indian -  {str(names[i])}")
#     plt.ylabel('CTD Temperature')
#     plt.xlabel('Salinity (PSU)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/WaterMasses/Indian_Ocean_{names[i]}.png')
#     plt.close()
#
#
# pacific = df.loc[df['Ocean_Label'] == 'Atlantic']
# names = np.unique(pacific['Water Mass'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass'] == names[i]]
#
#     fig = plt.figure(figsize=(12,6))
#     gs = gridspec.GridSpec(2, 4)
#     gs.update(wspace=.6, hspace=.6)
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#     plt.scatter(this_wm['LATITUDE'], this_wm['CTDPRS'], c=this_wm['DELC14'], cmap='magma')
#     plt.ylim(4000, 0)
#     plt.xlim(-70, 70)
#     plt.title(f"Atlantic -  {str(names[i])}")
#     plt.ylabel('Depth (CTD Pressure)')
#     plt.xlabel('Latitude')
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
#     plt.scatter(this_wm['SALNTY'], this_wm['CTDTMP'], c=this_wm['DELC14'], cmap='magma')
#     plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270)
#     plt.title(f"Atlantic -  {str(names[i])}")
#     plt.ylabel('CTD Temperature')
#     plt.xlabel('Salinity (PSU)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/WaterMasses/Atlantic_Ocean_{names[i]}.png')
#     plt.close()
#

