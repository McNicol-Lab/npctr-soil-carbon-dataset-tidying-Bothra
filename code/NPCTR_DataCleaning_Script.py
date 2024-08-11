# title: "NPCTR_DataCleaning_Script"
# author: "Aarin Bothra"
# date: '2024-08-10'

#import pandas, sql and numpy
import pandas as pd
from pandasql import sqldf
import numpy as np

# functions
def check(df):
    """
    confirms that for each pedon, there is only one master row
    
    :param df: dataframe that check runs on
    """ 
    
    # creates a dataframe of unique master rows
    unique_vals = df[['source', 'pedon_id']].drop_duplicates()
    errors = []

    # finds pedons with multiple master rows
    for index, data in unique_vals.iterrows():
        source = data['source']
        pid = data['pedon_id']
        sub = df.loc[(df['pedon_id'] == pid) & (df['source'] == source) & (df['pedon_start']==True)]
        if len(sub) != 1:
            errors.append(f'source {source} pid {pid} has {len(sub)} parent rows')

    # prints errors and number of errors
    print(len(errors))
    print('\n'.join(errors))

def fillPedonId(df):
    """
    fills the pedon id so that it is consistent through a dataset
    
    :param df: dataframe that fillPedonId runs on
    """ 

    # takes pedon id from master row and adds to all subordinate rows
    last_seen = 'Unknown_Pedon_ID'
    for index, data in df.iterrows():
        pid = data['ID']
        if not pd.isnull(pid) :
            last_seen = pid
        else:
            df.loc[index, 'ID'] = last_seen

def generatePedonStart(df):
    """
    creates boolean column pedon_start that denotes the master row
    
    :param df: dataframe that generatePedonStart runs on
    """ 

    # determines pedon_start based on total_c_1m column
    df['pedon_start'] = np.where(~df['total_c_1m'].isna(), True, False)

    unique_vals = df[['source', 'pedon_id']].drop_duplicates()

    # cleans the pedon_start column to get rid of irregularities
    for index, data in unique_vals.iterrows():
        source = data['source']
        pid = data['pedon_id']
        sub = df.loc[(df['pedon_id'] == pid) & (df['source'] == source) & (df['pedon_start']==True)]
        if len(sub) == 0:
            allsub = df.loc[(df['pedon_id'] == pid) & (df['source'] == source)]
            if len(allsub) > 0:
                df.loc[allsub.index[0], 'pedon_start'] = True

def generateHorizonNumber(df):
    """
    creates column horizon_number that denotes the order of the subordinate rows
    
    :param df: dataframe that generateHorizonNumber runs on
    """ 
    
    # calculates the horizon number 
    df['horizon_number'] = 0
    unique_vals = df[['source', 'pedon_id']].drop_duplicates()
    for index, data in unique_vals.iterrows():
        source = data['source']
        pid = data['pedon_id']
        sub = df.loc[(df['pedon_id'] == pid) & (df['source'] == source)]
        i=1
        for index, data in sub.iterrows():
            df.loc[index, "horizon_number"] = i
            i=i+1

def generatePedonTable(df):
    """
    creates the Pedon Table which only has pedon-specific data
    
    :param df: dataframe that generatePedonTable runs on
    :return: returns pedon table as Pandas dataframe
    """ 
    
    # creates subset df with pedon-specific data
    pedon = df.loc[df['pedon_start']].copy()
    pedon.reset_index(drop=True, inplace=True)
    pedon.drop(columns={'horizon_number', 'horizon', 'horizon_type', 'depth1', 'depth2', 'depth', 'bulk_density', 'bd_method', 'cf', 'cf_method', 'cconc', 'cconc_method', 'ccontent', 'ccontent_1m', 'pedon_start'}, inplace=True)
    return pedon    

def generateHorizonTable(df):
    """
    creates the Horizon Table which only has horizon-specific data
    
    :param df: dataframe that generateHorizonTable runs on
    :return: returns horizon table as Pandas dataframe
    """ 

    # creates subset df with horizon-specific data
    horizon = df.copy()
    horizon.drop(columns={'lat', 'lon', 'latlon_q', 'mineral_d', 'ff_d', 'total_d', 'total_c', 'total_c_1m','pedon_start'}, inplace=True)
    return horizon    

def generateSummaryTable(df):
    """
    creates the Summary Table which only has summary data
    
    :param df: dataframe that generateSummaryTable runs on
    :return: returns summary table as Pandas dataframe
    """ 

    # creates subset df with summary data
    summary = df.copy()
    summary.drop(columns={'horizon_type', 'depth1', 'depth2', 'depth', 'latlon_q', 'mineral_d', 'ff_d', 'total_d', 'bulk_density', 'bd_method', 'cf', 'cf_method', 'cconc', 'cconc_method', 'pedon_start'}, inplace=True)
    return summary 

# import all data
# 1. import data from dataframes 1,3,4,6,7
# 2. import and clean data from dataframe 2
# 3. import and clean data from dataframe 5
# 2. import and clean data from dataframe 8

# 1. dataframes 1,3,4,6,7
dataframe_1 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/SandbornLewis_1.csv")
dataframe_3 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/Calvert_3.csv")
dataframe_4 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/CalvertAdditional_4.csv")
dataframe_6 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/SEAK_6_Extended.csv")
dataframe_7 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/D'Armore_7.csv")

# 2. dataframe 2
dataframe_2 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/Kranabetter_2.csv")
fillPedonId(dataframe_2)

# 3. dataframe 5
dataframe_5_1 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/Shaw Full Profiles_5.csv")
dataframe_5_2 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/Shaw (only sites)_5.csv")
dataframe_5_1.rename(columns={"LOCATION_ID":"ID"}, inplace=True)
dataframe_5 = pd.merge(dataframe_5_1, dataframe_5_2, left_on='ID', right_on='ID', how='left')
dataframe_5.loc[pd.isnull(dataframe_5['TOTAL_C']), ['MINERAL_D','FF_D','TOTAL_D','TOTAL_C_1M_y','TOTAL_C_1M_CFADJ']] = None
dataframe_5.loc[dataframe_5.SOURCE.isnull(), 'SOURCE'] = 'Unknown Source'

# 4. dataframe 8
dataframe_8 = pd.read_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/NPCTR-Cleaning/BEC_8.csv")
dataframe_8.SOURCE = 'BEC (Meidinger and Pojar, 1991)'
dataframe_8.loc[(dataframe_8['ID'] == 158) & (dataframe_8['BEC Number'] == 741), 'ID'] = 158741
dataframe_8.loc[(dataframe_8['ID'] == 263) & (dataframe_8['BEC Number'] == 420), 'ID'] = 263420

# rearrange and clean separate dataframes
# 1. remove all spaces from column names
# 2. rename columns to standardize names
# 3. concat data to master dataframe

# 1. strips all spaces
all = [dataframe_1, dataframe_2, dataframe_3, dataframe_4, dataframe_5, dataframe_6, dataframe_7, dataframe_8]
for df in all:
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.strip()

# 2. standardizes column names
dataframe_5.rename(columns={"upper_hzn_limit":"depth2", "hzn_thickness":"depth", "bulk_density":"bulk density", "cf_final":"cf", "org_carb_pct":"cconc", "hzn_org_min":"horizon_type", "total_c_1m_cfadj":"total_c_1m",  "db_meas_est":"bd_method", "carb_meas_est":"cconc_method"}, inplace=True)
dataframe_6.drop(columns={"horizon", "order"}, inplace=True)
dataframe_6.rename(columns={"unnamed: 26": "total_c_1m_2","canadian order":"order","horizon.1":"horizon"}, inplace=True)
dataframe_7.rename(columns={"mincont":"cf"}, inplace=True)
dataframe_8['horizontype'] = dataframe_8['horizontype'].replace(1.0, 'Organic')
dataframe_8['horizontype'] = dataframe_8['horizontype'].replace(2.0, 'Mineral')
dataframe_8.rename(columns={"order_only":"order", "upperdepth":"depth2", "lowerdepth":"depth1", "new.cconc":"cconc", "bulk.density":"bulk density", "ff_d":"ff_d_individual", "ff_d.1":"ff_d", "horizontype":"horizon_type"}, inplace=True)

# 3. creates master dataframe
carbon = pd.concat([dataframe_1, dataframe_2, dataframe_3, dataframe_4, dataframe_5, dataframe_6, dataframe_7, dataframe_8], ignore_index=True)
carbon.rename(columns={"id":"pedon_id", "bulk density":"bulk_density"}, inplace=True)
generatePedonStart(carbon)
generateHorizonNumber(carbon)

# rearrange and clean master dataframe
# 1. create cf_method column
# 2. create cconc_method column
# 3. create bd_method column
# 4. drop unneeded columns 
# 5. fill and standardize latlon_q column

# 1. cf_method
carbon.loc[carbon.source.isin(['BEC (Meidinger and Pojar, 1991)', 'Shaw et al. 2005', 'Siltanen et al. 1997', 'Moon &  Selby 1988 Rep 64', 'Van Vliet et al. 1987 Rep bc43-1', 'Kenney et al. 1988 Rep bc43-2', 'Oswald 1973 Rep BC-43', 'Inselberg et al. 1982 Land Mgmt Rep. 12', 'LEWIS 1976']), 'cf_method'] = 1
carbon.loc[carbon['cf'].isnull(), 'cf_method'] = 2
carbon['cf'] = carbon['cf'].fillna(0)
carbon.loc[carbon['cf_method'].isnull(), 'cf_method'] = 0

# 2. cconc_method
carbon['cconc_method'] = carbon['cconc_method'].replace('Measured', 0)
carbon['cconc_method'] = carbon['cconc_method'].replace('Estimated', 1)
carbon.loc[carbon.source.isin(['BEC (Meidinger and Pojar, 1991)', "D'Amore & Lynn (2002)"]), 'cconc_method'] = 2
carbon.loc[carbon['depth of mean'].isnull() == False, 'cconc_method'] = 2
carbon.loc[carbon['cconc_method'].isnull(), 'cconc_method'] = 0

# 3. bd_method
carbon['bd_method'] = carbon['bd_method'].replace('Measured', 0)
carbon['bd_method'] = carbon['bd_method'].replace('Estimated', 1)
carbon.loc[carbon['bulk density_meas'] == 0, 'bd_method'] = 1
carbon.loc[carbon['source'] == 'BEC (Meidinger and Pojar, 1991)', 'bd_method'] = 1 #needs to be confirmed
carbon.loc[carbon['bd_method'].isnull(), 'bd_method'] = 0

# 4. drops columns
carbon.dropna(how="all", axis=1, inplace=True)
carbon.drop(columns={"row", "next", "slope", "aspect", "elevation", "cconc_slope", "depth of mean", "real depth", "1/-trendline slope", "horizon_id", "cf_class", "cf_vol_pct", "bulk density_meas", "bulk density_shaw", "bec number", "surficialmaterialsurf", "zone", "ff_d_individual", "texture", "min_d", "total_c_1m_2", "ggroup_exp", "total_c_1m_x", "total_c_1m_y", "db_est_type", "ccontent", "total_c", "ccontent_1m", "total_c_1m"}, inplace=True)

# 5. latlon_q
low_quality = sqldf("SELECT DISTINCT pedon_id from carbon WHERE latlon_q = 'NO'")['pedon_id'].tolist()
high_quality = sqldf("SELECT DISTINCT pedon_id from carbon WHERE latlon_q = 'YES' OR latlon_q = 'HIGH'")['pedon_id'].tolist()
carbon.loc[carbon.pedon_id.isin(low_quality), 'latlon_q'] = "LOW"
carbon.loc[carbon.pedon_id.isin(high_quality), 'latlon_q'] = "HIGH"

# calculate carbon stock columns
# 1. calculate ccontent
# 2. calculate total_carbon
# 3. calculate ccontent_1m
# 4. calculate total_carbon_1m
# 5. round calculations

# 1. ccontent
carbon['ccontent'] = round((carbon['cconc']/100)*carbon['bulk_density']*carbon['depth']*((100-carbon['cf'])/100)*10000)

# 2. total_carbon
total_carbon = carbon.groupby('pedon_id')['ccontent'].sum().reset_index()
total_carbon.rename(columns={'ccontent':'total_c'}, inplace=True)
carbon = carbon.merge(total_carbon, how='left', on='pedon_id')
carbon.loc[~carbon['pedon_start'], 'total_c'] = np.nan

# 3. ccontent_1m
carbon['ccontent_1m'] = np.where(
    (carbon['depth1'] <= -100) | (carbon['depth1'] >= 100),
    np.where(
        (carbon['ccontent'] - carbon['ccontent'] * (abs(carbon['depth1']) - 100) / (abs(carbon['depth1']) - abs(carbon['depth2']))).round() < 0,
        0,
        (carbon['ccontent'] - carbon['ccontent'] * (abs(carbon['depth1']) - 100) / (abs(carbon['depth1']) - abs(carbon['depth2']))).round()
    ),
    carbon['ccontent']
)

# 4. carbon_total_1m
total_carbon_1m = carbon.groupby('pedon_id')['ccontent_1m'].sum().reset_index()
total_carbon_1m['ccontent_1m'] *= 0.01
total_carbon_1m.rename(columns={'ccontent_1m':'total_c_1m'}, inplace=True)
carbon = carbon.merge(total_carbon_1m, how='left', on='pedon_id')
carbon.loc[~carbon['pedon_start'], 'total_c_1m'] = np.nan

# 5. rounds
carbon[['total_c_1m', 'total_c']]=carbon[['total_c_1m', 'total_c']].round(2)
carbon[['bd_method', 'cf_method', 'cconc_method']] = carbon[['bd_method', 'cf_method', 'cconc_method']].astype(int)

#save and export data
# 1. reorder columns
# 2. export master table to csv
# 3. export pedon table to csv
# 4. export horizon table to csv
# 5. export summary table to csv
# 6. export all four tables to xlsx
# 7. prints and check the data

# 1. reorders
carbon = carbon[['source', 'pedon_id', 'order', 'lat', 'lon', 'latlon_q', 'horizon_number', 'horizon' , 'horizon_type', 'depth2', 'depth1', 'depth', 'bulk_density', 'bd_method', 'cf', 'cf_method', 'cconc', 'cconc_method', 'mineral_d', 'ff_d', 'total_d',  'ccontent', 'total_c', 'ccontent_1m', 'total_c_1m', 'pedon_start']]

# 2. master table
carbon.to_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/Output/NPCTRMasterTable.csv", index_label='id')

# 3. pedon table
pedon = generatePedonTable(carbon)
pedon.to_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/Output/NPCTRPedonTable.csv", index_label='id')

# 4. horizon table
horizon = generateHorizonTable(carbon)
horizon.to_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/Output/NPCTRHorizonTable.csv", index_label='id')

# 5. summary table
summary = generateSummaryTable(carbon)
summary.to_csv("/Users/aarinbothra/dropbox/aarin/NPCTR_Research/Output/NPCTRSummaryTable.csv", index_label='id')

# 6. xlsx file
with pd.ExcelWriter('/Users/aarinbothra/dropbox/aarin/NPCTR_Research/Output/npctr-soil-carbon-dataset-2024.xlsx') as writer:  
    carbon.to_excel(writer, sheet_name='MasterTable', index=False)
    pedon.to_excel(writer, sheet_name='PedonTable', index=False)
    horizon.to_excel(writer, sheet_name='HorizonTable', index=False)
    summary.to_excel(writer, sheet_name='SummaryTable', index=False)

# 7. prints and checks
print(carbon)
check(carbon)