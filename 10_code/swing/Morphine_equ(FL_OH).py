# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import warnings 
warnings.filterwarnings('ignore')
#read the opioid shipment data and FIPS code data
data = pd.read_csv('arcos-fl-statewide-itemized.tsv',delimiter = '\t')
data2 = pd.read_csv('arcos-oh-statewide-itemized.tsv',delimiter = '\t')
FIPS = pd.read_excel('fips_codes_website.xls')
#take a look at the data
data.head()
#get the columns we want
drug_data = data[['BUYER_COUNTY','TRANSACTION_DATE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor']]
#Check the null values. 
#We have a small amount of missing data.Dropping it will not make large effects on the final results
drug_data.isnull().sum()
drug_data.dropna(inplace = True) 
#Transform the FIPS code data to the format we want
def trans_code(a):
    """transform code in the same format"""
    if a < 10:
        str_a = str(a)
        b = '00'+str_a
    elif a <100:
        str_a = str(a)
        b = '0'+str_a
    else:
        b =str(a)
        
    return b

def trans_state(a):
    """transform code in the same format"""
    if a < 10:
        str_a = str(a)
        b = '0'+str_a
    else:
        b =str(a)
        
    return b
#make six digits code
county = FIPS[FIPS['Entity Description']=='County']
county['County FIPS Code'] = county['County FIPS Code'].apply(trans_code)
county['State FIPS Code'] = county['State FIPS Code'].apply(trans_state)
county['County_FIPS'] = county['State FIPS Code'] +county['County FIPS Code'] 
#Obtain FL drug data with FIPS
FL_FIPS = county[county['State Abbreviation'] == 'FL']
FL_FIPS['GU Name'] = FL_FIPS['GU Name'].str.replace('St.','SAINT')
FL_FIPS['GU Name'] = FL_FIPS['GU Name'].str.upper()
FL_FIPS_code = FL_FIPS[['GU Name','County_FIPS']]
#Merge FIPS code with drug table
FL_drug = pd.merge(FL_FIPS_code,drug_data,left_on = 'GU Name', right_on = 'BUYER_COUNTY',how = 'right')
#There are some discrepancies in the FIPS data and shippment data.
#We need to input some FIPS code by hand
FL_drug['GU Name'].unique()
FL_drug['BUYER_COUNTY'].unique()
 #Fill the missing FIPS code for some counties
FL_drug[FL_drug['BUYER_COUNTY'] == 'DUVAL'] = FL_drug[FL_drug['BUYER_COUNTY'] == 'DUVAL'].fillna('12031')
FL_drug[FL_drug['BUYER_COUNTY'] == 'DE SOTO'] = FL_drug[FL_drug['BUYER_COUNTY'] == 'DE SOTO'].fillna('12029')
#drop duplicated columns
FL_drug.drop(columns = 'GU Name',inplace = True)
#transform Date to year
def trans_year(date):
    
    date_str = str(date)
    year = date_str[-4:]
    return year
FL_drug['Year'] = FL_drug['TRANSACTION_DATE'].apply(trans_year)
FL_drug.drop(columns = 'TRANSACTION_DATE',inplace = True)
#Obtain Morphine_equ
FL_drug['Morphine_equ'] = FL_drug['CALC_BASE_WT_IN_GM'] * FL_drug['MME_Conversion_Factor']
FL_drug['State'] = 'FL'
#Groupby County and Year
FL_drug_grouped = FL_drug[['County_FIPS','BUYER_COUNTY','Year','Morphine_equ']]
FL_grouped = FL_drug_grouped.groupby(['Year','County_FIPS','BUYER_COUNTY']).sum()
FL_grouped = FL_grouped.reset_index()
#Take a look at the data
FL_grouped.head()
#Apply the same procedure on data2(GA data)
drug_data2 = data2[['BUYER_COUNTY','TRANSACTION_DATE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor']]
drug_data2.isnull().sum() #Drop 23 missing data
drug_data2.dropna(inplace = True)
#Obtain OH drug data with FIPS
OH_FIPS = county[county['State Abbreviation'] == 'OH']
OH_FIPS['GU Name'] = OH_FIPS['GU Name'].str.upper()
OH_FIPS_code = OH_FIPS[['GU Name','County_FIPS']]
OH_drug = pd.merge(OH_FIPS_code,drug_data2,left_on = 'GU Name', right_on = 'BUYER_COUNTY',how = 'right')
OH_drug['GU Name'].unique()
OH_drug['BUYER_COUNTY'].unique()
#There are no missing data
#drop duplicated columns
OH_drug.drop(columns = 'GU Name',inplace = True)
OH_drug['Year'] = OH_drug['TRANSACTION_DATE'].apply(trans_year)#GET year
OH_drug.drop(columns = 'TRANSACTION_DATE',inplace = True)
OH_drug['Morphine_equ'] = OH_drug['CALC_BASE_WT_IN_GM'] * OH_drug['MME_Conversion_Factor']
OH_drug['State'] = 'OH'
#Groupby County and Year
OH_drug_grouped = OH_drug[['County_FIPS','BUYER_COUNTY','Year','Morphine_equ']]
OH_grouped = OH_drug_grouped.groupby(['Year','County_FIPS','BUYER_COUNTY']).sum()
OH_grouped = OH_grouped.reset_index()
#Take a look at the data
OH_grouped.head()