"""
OLD OLD OLD
"""

# import pandas as pd
# import numpy as np
# import warnings
# from blank_corr_functions import long_date_to_decimal_date
# warnings.simplefilter("ignore")
#
# """
# This script calculates MCC values for different data types for XCAMS blank correction.
# This script has been tested to capture the same blanks as the following past wheels:
#
# """
# # ask the user to input the TW# of the current wheel.
# input_name = input("What is the TW of this wheel?")
#
# # read in all the excel files I'll need and drop empty lines
# df = pd.read_excel(r'I:\C14Data\C14_blank_corrections_dev\TW{}.xlsx'.format(input_name)).dropna(subset='Job::Sample Type From Sample Table').reset_index(drop=True)  # grab the file that has been exported from RLIMS, thanks to Valerie's new button.
# stds_hist = pd.read_excel(r'I:\C14Data\C14_blank_corrections_dev\TW{}standards.xlsx'.format(input_name)).dropna(subset='Date Run').reset_index(drop=True)  # Read in the standards associated with it.
# refs = pd.read_excel(r'I:\C14Data\C14_blank_corrections_dev\Pretreatment_reference.xlsx').dropna(subset='R number to correct from')  # Grab a small file I made that associates samples types to R numbers for correction
#
# # this line checks that no standards in the list are LARGER than the largest TP # in the wheel (can't use future data to correct present wheel (NOT WORKING...)
# # max_TP = max(df['TP'])
# # stds_hist = stds_hist.loc[stds_hist['TP'] < max_TP]
#
# sample_type_list = np.unique(df['Job::Sample Type From Sample Table'])  # saving this list to write to a file later
#
# """
# Lets write a summary template file which will be pasted into RLIMS
# """
# f = open(r'I:/C14Data/C14_blank_corrections_dev/PythonOutput/TW{}_summary.txt'.format(input_name), 'w')
# """
# Lets check how the OX-1's performed.
# """
# primary_standards = df.loc[df['Job::Sample Type From Sample Table'] == 'Oxalic']  # grab all the ROWS where the AMS category is XCAMS
# prim_std_average = np.average(primary_standards['Ratio to standard'])
# prim_std_1sigma = np.std(primary_standards['Ratio to standard'])
# prim_std_13average = np.average(primary_standards['delta13C_AMS'])
# prim_std_13_1sigma = np.std(primary_standards['delta13C_AMS'])
# rounding_decimal = 3  # Note: if the rounding decimal is around 3, but the result comes out to 1.0, this is because it has rounded up from 0.99999 or so, for example.
#
# # Do any of the OX-1's deviate from their IRMS number?
# # Compare 13C AMS to 13C IRMS
# arr1 = []  # initialize a few empty arrays for later use
# arr2 = []
# C13_threshold = 5
# for i in range(0, len(primary_standards)):
#     row = primary_standards.iloc[i]  # access the first row
#     ams = row['delta13C_AMS']
#     ams_err = row['delta13C_AMS_Error']
#     irms = row['delta13C_IRMS']
#     irms_error = row['delta13C_IRMS_Error']
#     delta = abs(ams - irms)
#
#     if delta >= C13_threshold:
#         arr1.append(delta)
#         arr2.append(row['TP'])
#
# result = pd.DataFrame({"TP": arr2, "Absolute value, (AMS - IRMS 13C)": arr1})
#
#
# print(("The types of Oxalic I's in this wheel are {} ".format(np.unique(primary_standards['Description from Sample']))), file = f)
# print(("The average RTS of the Primary Standards in this wheel is {} \u00B1 {}".format(round(prim_std_average, rounding_decimal),round(prim_std_1sigma, rounding_decimal))), file = f)
# print(("The average OX-1 13C values in this wheel is {} \u00B1 {}".format(round(prim_std_13average, rounding_decimal), round(prim_std_13_1sigma, rounding_decimal))), file = f)
# print()
#
# if len(result) > 0:
#     print(("The following standards are outside the selected range of {}\u2030 difference between IRMS and AMS 13C".format(C13_threshold)), file = f)
#     print((result), file = f)
# else:
#     print(("No OX-1's 13C values deviate from IRMS 13C values more than {}\u2030 ".format(C13_threshold)), file = f)
#     print()
# # </editor-fold>
#
#
# # <editor-fold desc="Break up wheel based on different types of graphite">
#
# """
# This next block of code searches the standards extracted from the database, and find the MCC related to each of the items on my "Pretreatment_reference" excel sheet
# It will find an MCC for all types of standards, even if those are not used on the wheel. This MCC will be referred to later when we add it onto the samples.
#
# The next few lines that have been commented out are so beacuse it takes the longest to actually load the standard data. When the code is done and dusted, I will uncomment these out
# But for now, it's silly to wait every time to load so much data when I'm working on other parts of the script
# """
# x = stds_hist['Date Run']
# stds_hist['Date Run'] = long_date_to_decimal_date(x)                     # This line converts the dates to "Decimal Date" so that I can find only dates that are 0.5 years max before most recent date
# date_bound_input = input("How far back do you want the standards to go? Type 0.5 for 1/2 year, and 1 for 1 year")
# date_bound = max(stds_hist['Date Run']) - np.float(date_bound_input)
# stds_hist = stds_hist.loc[(stds_hist['Date Run'] > date_bound)]      # Index: find ONLY dates that are more recent than 1/2 year
#
# stds_hist = stds_hist.loc[(stds_hist['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag
# stds_hist = stds_hist.loc[(stds_hist['wtgraph'] > 0.3)]  # Drop everything that is smaller than 0.3 mg.
# stds_hist = stds_hist.loc[(stds_hist['Ratio to standard'] < 0.1)]  # Drop all blanks that are clearly WAY too high
# stds_hist = stds_hist.loc[(stds_hist['Category In Calculation'] != 'Background Test')]  # Drop all background tests
# # decide if there are any standards we want to avoid
#
# yn = input("Are there any standards you specifically want to exclude? (y/n)")
# if yn == 'y':
#     n = int(input("Enter the number of standards you will exclude: "))
#     print("\n")
#     num_list = list(int(num) for num in input("Enter the TP numbers, each separated by space ").strip().split())[:n]
#     print("User list: ", num_list)
#     for i in range(len(num_list)):
#         stds_hist = stds_hist.loc[(stds_hist['TP'] != num_list[i])]
#
# """
# This next block of code will search through all the R numbers in my pretreatment reference file.
# It will calculate the MCC and 1-sigms std of all acceptable standards and attach that MCC to that R number. Later,
# this number will be matched to unknowns with the same pretreatment process, and the MCC tacked onto the unknowns.
# """
#
# mcc_array = []
# mcc_1sigma_array = []
# stringarray = []
# stds_dataframe = pd.DataFrame({})
# for i in range(0, len(refs['Sample Type From Sample Table'])):            # run through the list of "Sample Type from Sample Table" in the Pretreatement Reference list
#     ref_row = refs.iloc[i]                                                # grab the first row of Pretreatment Reference list
#     this_R = (ref_row['R number to correct from'])                        # find the R number associated with that blank correction reference
#     current_standards = stds_hist.loc[(stds_hist['R_number'] == this_R)]  # find all standards that match the current R number I'm interetsed in from the reference table
#     stds_dataframe = pd.concat([stds_dataframe, current_standards])
#     mcc = np.average(current_standards['Ratio to standard'])              # Calculate the average RTS of these specific standards in this sub-loop, and its standard deviation
#     mcc_1sigma = np.std(current_standards['Ratio to standard'])
#     mcc_array.append(mcc)                                                 # tack these values onto an array, which we can add to the reference dataframe in a few lines
#     mcc_1sigma_array.append(mcc_1sigma)
#
#     # now I need to add the tilda's to tell which standards were used in each case
#     strings = ""
#     TPs = current_standards['TP'].reset_index(drop=True)
#     for m in range(len(TPs)):
#         q_o = TPs[m]
#         strings = strings + str(int(q_o)) + str("\u007e")
#     stringarray.append(strings)
#
# refs['MCC'] = mcc_array
# refs['MCC_1sigma'] = mcc_1sigma_array
# refs['Stds_used'] = stringarray
# # refs.to_excel(r'C:/Users/clewis/IdeaProjects/GNS/Blank_Corrections/Output_results/Refscheck.xlsx'.format(input_name), sheet_name='Sheet_name_1')
# """
# This set of nested loops will iterate through each row of wheel's data, and find the samples type. Then, it will iterate
# through the pretreatment reference list. When it finds a sample type that matches, it takes the calculated MCC and associated
# data and tacks it onto that wheel's data for re-uploading into RLIMS. If no matches are found (OX-1's, sucrose, kapuni), it
# inserts -999.
# """
#
# mcc_arr2 = []
# mcc_1sigma2 = []
# r_arr = []
# pretreatment = []
# stds_used = []
# not_found = []
#
# df = df.loc[(df['Description from Sample'] != 'Kapuni CO2 cylinder')]  # remove the Kapuni and the sucrose
# df = df.loc[(df['Description from Sample'] != 'ANU Sucrose - IAEA C6')]
# df = df.loc[(df['Category In Calculation'] != 'Background Test')]
# df = df.loc[(df['Job::Sample Type From Sample Table'] != 'other organic material')]
#
# for k in range(0, len(df)):
#     data_row = df.iloc[k]  # grab the first row of data
#     sample_type = str(data_row['Job::Sample Type From Sample Table'])
#     flag = 0
#     for q in range(0, len(refs)):
#         ref_row = refs.iloc[q]  # run through the references to find the right MCC
#         standard_type = str(ref_row['Sample Type From Sample Table'])
#         # print(standard_type)
#
#         if sample_type == standard_type:  # when the sample type matches the standard type,
#             # print('I found a match: {}'.format(sample_type))
#             mcc_arr2.append(ref_row['MCC'])
#             mcc_1sigma2.append(ref_row['MCC_1sigma'])
#             r_arr.append(ref_row['R number to correct from'])
#             pretreatment.append(ref_row['Pre-treatment Type'])
#             stds_used.append(ref_row['Stds_used'])
#             flag = 1  # tells the computer if a match was found
#
#     if flag == 0:                        # if a match was not found, check if it was used for primary standards, or tuning, then fill with -999
#         if sample_type == 'Oxalic':
#             mcc_arr2.append(-999)
#             mcc_1sigma2.append(-999)
#             r_arr.append(-999)
#             pretreatment.append(-999)
#             stds_used.append(-999)
#         else:
#             not_found.append(sample_type)
#             mcc_arr2.append(-999)
#             mcc_1sigma2.append(-999)
#             r_arr.append(-999)
#             pretreatment.append(-999)
#             stds_used.append(-999)
#
# if len(not_found) > 0:
#     print((f"Sample with type {not_found} could not be matched with a corresponding R number for correction."
#           f"Please add these sample types with corresponding R number in Pretreatment_reference.xlsx and re-run the script"), file = f)
#
# df['MCC'] = mcc_arr2
# df['MCC_1sigma'] = mcc_1sigma2
# df['R numbers used for blank correction'] = r_arr
# df['Pretreatment type'] = pretreatment
# df['Standards used'] = stds_used
#
# stds_dataframe = stds_dataframe.drop_duplicates(subset = 'TP', keep='first')
# with pd.ExcelWriter(r'I:/C14Data/C14_blank_corrections_dev/PythonOutput/TW{}_results.xlsx'.format(input_name)) as writer:
#
#     # use to_excel function and specify the sheet_name and index
#     # to store the dataframe in specified sheet
#     refs.to_excel(writer, sheet_name="Current MCCs", index=False)
#     df.to_excel(writer, sheet_name="TW{}_results".format(input_name), index=False)
#     stds_dataframe.to_excel(writer, sheet_name="Current MCC Details", index=False)
#     """
#     This next line will write the details of all the stds used for MCC calculation, but I need to clean it up slightly first.
#     """
#
# # </editor-fold>
#
#
# print('TW{} measurement:'.format(input_name), file = f)  # writes title
# print("", file = f)
# print('This wheel contains the following types of graphite: {}'.format(sample_type_list), file = f)  # writes title
# print("", file = f)
# print('CalAMS error adjustments: ', file = f)
# print('*None Needed', file = f)
#
# print("", file = f)
# print('Primaries:', file = f)
# print('* OX-1 Cathodes', file = f)
# print('_______{} cathodes used'.format(len(primary_standards['TP'])
#                                                         ), file = f)
# print('_______All accepted', file = f)
# print("", file = f)
# print('Secondaries:', file = f)
# print("", file = f)
# print("", file = f)
# print('Blanks', file = f)
# print("", file = f)
# print("", file = f)
# print('Unknowns', file = f)
# print("", file = f)
# print("", file = f)