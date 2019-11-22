#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[3]:


#read each of the .csv tables
#validated these are correct
fl_equ = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-4/master/20_intermediate_files/FL_opioid_equ.csv?token=AMVJ2QKKKXA2KERBXWYKPNC5ZVR7K')
ga_equ = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-4/master/20_intermediate_files/GA_opioid_equ.csv?token=AMVJ2QNATVTFJ76YJUVZMUC5ZVSBE')
counties = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-4/master/20_intermediate_files/Counties_DF_Merge_Ready_v2.csv?token=AMVJ2QODBV4X3BIX6NZLGPK5ZVR3M')
deaths = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-4/master/20_intermediate_files/overdose_deaths.csv?token=AMVJ2QP2BOWXM27YNZG2MJ25ZVSDA')
controls = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-4/master/20_intermediate_files/State_Opioid_Controls_Year_Changed.csv?token=AMVJ2QO3PKYYKA6DGMJHH6K5ZVSJA')


# In[4]:


#Dekalb was a problem county, changed name in counties to be without a space
counties = counties.replace(to_replace = 'DE KALB', value = 'DEKALB')


# In[5]:


counties['State'].value_counts().sum()


# In[6]:


deaths.sample(20)


# In[7]:


#merge the counties and population data with the control states table
outer_counties = controls.merge(counties, how = 'outer', on = 'State', indicator = True )


# In[8]:


outer_counties.head()
#outer_counties.sample(50)
#outer_counties.describe()
#outer_counties._merge.value_counts()


# In[9]:


#outer_counties['Year'].dtypes


# In[10]:


#Clean the death data table to replace County, Borough, Parish, and city with '' and make them upper case
deaths['County'] = deaths['County'].replace(regex = True, to_replace = [' County', ' Borough', ' Parish', ' City'], value = '')
deaths['County'] = deaths['County'].replace(regex = True, to_replace = ['St. '], value = 'Saint ')
deaths['County'] = deaths['County'].str.upper()
deaths['Year'] = deaths['Year'].astype(int)
#Confirmed the changes were correct


# In[11]:


deaths.sample(10)
#outer_counties.sample(10)


# In[12]:


#drop indicator column
outer_counties = outer_counties.drop(axis = 1, columns = '_merge')


# In[13]:


death_added = deaths.merge(outer_counties, how = 'outer', on = ['State', 'Year', 'County'], indicator = True)
death_added._merge.value_counts()
#death_added.sample(10)
#This resulted in less left_only joins than expected, but this is because not all counties have death data for drug overdoses


# In[14]:


death_added['Year'].value_counts().sum()


# In[15]:


death_added.sample(20)


# In[16]:


#rename columns to match with the intermediate merged table for Florida
fl_equ = fl_equ.rename(columns = {'BUYER_COUNTY':'County', 'County_FIPS':'FIPS'})
fl_equ.head()


# In[17]:


#rename columns to match with the intermediate merged table for Georgia
ga_equ = ga_equ.rename(columns = {'BUYER_COUNTY':'County', 'County_FIPS':'FIPS'})
ga_equ.head()


# In[18]:


#drop indicator column from death_added
death_added = death_added.drop(axis = 1, columns = '_merge')


# In[19]:


#merge florida morphine and georgia morphine
#Expect only left or right merges
m_combined = ga_equ.merge(fl_equ, how = 'outer', on = ['County', 'State', 'Morphine_equ','FIPS', 'Year'], indicator = True)
m_combined.sample(10)


# In[20]:


m_combined.head()


# In[21]:


death_added.sample(10)


# In[22]:


#check merge
#Validated, similar to expected counts
m_combined._merge.value_counts()


# In[23]:


#drop _merge column
m_combined = m_combined.drop(axis = 1, columns = '_merge')


# In[24]:


#add the morphine table into the intermediate table
morphine_added = m_combined.merge(death_added, how = 'outer', on = ['County', 'State', 'FIPS','Year'], indicator = True)
#morphine_added.describe()
morphine_added._merge.value_counts()
#morphine_added.loc[:, 'Year'].value_counts()


# In[25]:


#We are not going to use Georgia Anyway for morphine checks
morphine_added_check = morphine_added.loc[((morphine_added['County'] == 'MUSCOGEE'))]
morphine_added_check.head()


# In[26]:


morphine_added[morphine_added._merge == 'left_only']


# In[27]:


morphine_added.head()


# In[28]:


morphine_added._merge.value_counts()


# In[29]:


#remove merge column
morphine_added = morphine_added.drop(axis = 1, columns = '_merge')


# In[30]:


#Drop the unnamed and index column, which was an index column left over from the import of an intermediate table
final_frame = morphine_added.drop(columns = 'Unnamed: 0')
final_frame = final_frame.drop(columns = 'index')
final_frame.sample(10)


# In[31]:


#add in a deaths per capita column
final_frame['Deaths_PC'] = final_frame['Deaths'] / final_frame['Population']
final_frame.sample(10)


# In[ ]:





# In[32]:


final_frame.loc[:,'Year'].value_counts()
final_frame.loc[:,'County'].value_counts()


# In[33]:


#export the final frame to a csv
#final_frame.to_csv('Final_Data_Frame_Python_Midterm.csv')


# In[34]:


#Check filter to see if it is reasonable


# In[35]:


ultimate_final_frame = final_frame.loc[(final_frame['State'] == 'CA') | (final_frame['State'] == 'AZ') | (final_frame['State'] == 'NM') | (final_frame['State'] == 'TX') | (final_frame['State'] == 'GA') | (final_frame['State'] == 'AL') | (final_frame['State'] == 'MS') | (final_frame['State'] == 'FL') | (final_frame['State'] == 'OR')| (final_frame['State'] == 'ID') | (final_frame['State'] == 'MO') | (final_frame['State'] == 'WA')]
ultimate_final_frame.sample(10)


# In[37]:


ultimate_final_frame.to_csv('ultimate_final_frame.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




