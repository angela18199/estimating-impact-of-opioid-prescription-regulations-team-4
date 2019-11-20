# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from plotnine import *
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import statsmodels.formula.api as smf

#import data
FL_drug = pd.read_csv('FL_opioid_equ.csv')
OH_drug = pd.read_csv('OH_opioid_equ.csv')
#rename columns to make data more consistent
FL_drug.rename(columns = {'County_FIPS':'FIPS','BUYER_COUNTY':'County'},inplace = True)
OH_drug.rename(columns = {'County_FIPS':'FIPS','BUYER_COUNTY':'County'},inplace = True)
#Take a look at the distribution
sns.kdeplot(FL_drug['Morphine_equ'],label = 'FL',color = 'b')
plt.show()
#From the density plot, most of the Morphine_equ data lie between 0 and 250000. Let's look at the samples with Morphine_equ larger than 1500000.
FL_drug[FL_drug['Morphine_equ']>1500000]
#Take a look at the interesting county
FL_drug[FL_drug['FIPS']==12086]
#Plot the distribution of OH
sns.kdeplot(OH_drug['Morphine_equ'],label = 'OH',color= 'y')
plt.show()
#randomly select 10 counties from FL and OH and plot their trends from 2006 to 2012.
FIPS_FL= np.array(FL_drug.FIPS.iloc[:])
FIPS_OH= np.array(OH_drug.FIPS.iloc[:])
rand_FL = np.random.randint(0,FIPS_FL.shape[0],10)
rand_OH = np.random.randint(0,FIPS_OH.shape[0],10)
for i in range(10):
    ind = rand_FL[i]
    county =  FL_drug[FL_drug.FIPS==FIPS_FL[ind]]
    plt.figure()
    sns.lineplot(county.Year,county.Morphine_equ)

for i in range(10):
    ind = rand_OH[i]
    county =  OH_drug[OH_drug.FIPS==FIPS_OH[ind]]
    plt.figure()
    sns.lineplot(county.Year,county.Morphine_equ)

#Groupby our data by year to see the overall change of the state
Mor_equ_FL = FL_drug.groupby('Year').mean()
Mor_equ_FL.reset_index(inplace = True)
#To make the change more clear, we use 'Years from Policy Change' instead of 'Year' to indicate time
Mor_equ_FL['Years from Policy Change'] = Mor_equ_FL.Year - 2010
Mor_equ_FL.head()
#Plot pre-post
plt.figure(figsize=(10,6))
sns.lineplot(Mor_equ_FL[Mor_equ_FL['Year']<=2009]['Years from Policy Change'],Mor_equ_FL['Morphine_equ'],color="green",label = 'pre')
sns.lineplot(Mor_equ_FL[Mor_equ_FL['Year']>2009]['Years from Policy Change'],Mor_equ_FL['Morphine_equ'],color="blue",label = 'post')
plt.axvline(x=0,linestyle = '-.',color = 'black')
plt.xlabel("Years from Policy Change",fontsize = 12)
plt.ylabel("Morphine_equ",fontsize = 12)
plt.title("Pre-Post Model Graph for FL",fontsize = 16)
plt.show()
#Prepare data for DID
Mor_equ_OH = OH_drug.groupby('Year').mean()
Mor_equ_OH.reset_index(inplace = True)
Mor_equ_OH['Years from Policy Change'] = Mor_equ_OH.Year - 2010
Mor_equ_OH.head()
#Plot DID model
plt.figure(figsize=(10,6))
sns.lineplot(Mor_equ_FL[Mor_equ_FL['Year']<=2009]['Years from Policy Change'],Mor_equ_FL['Morphine_equ'],color="green",label = 'FL')
sns.lineplot(Mor_equ_FL[Mor_equ_FL['Year']>2009]['Years from Policy Change'],Mor_equ_FL['Morphine_equ'],color="green")
sns.lineplot(Mor_equ_OH[Mor_equ_OH['Year']<=2009]['Years from Policy Change'],Mor_equ_OH['Morphine_equ'],color="blue",label = 'OH')
sns.lineplot(Mor_equ_OH[Mor_equ_OH['Year']>2009]['Years from Policy Change'],Mor_equ_OH['Morphine_equ'],color="blue")
plt.axvline(x=0,linestyle = '-.',color = 'black')
plt.xlabel("Years from Policy Change",fontsize = 12)
plt.ylabel("Morphine_equ",fontsize = 12)
plt.title("Difference in Difference Model between FL and OH",fontsize = 16)
plt.show()
#Set 2011 to be the policy change year, plot again
plt.figure(figsize=(10,6))
sns.lineplot(Mor_equ_FL[Mor_equ_FL['Year']<=2010]['Years from Policy Change'],Mor_equ_FL['Morphine_equ'],color="green",label = 'FL')
sns.lineplot(Mor_equ_FL[Mor_equ_FL['Year']>2010]['Years from Policy Change'],Mor_equ_FL['Morphine_equ'],color="green")
sns.lineplot(Mor_equ_OH[Mor_equ_OH['Year']<=2010]['Years from Policy Change'],Mor_equ_OH['Morphine_equ'],color="blue",label = 'OH')
sns.lineplot(Mor_equ_OH[Mor_equ_OH['Year']>2010]['Years from Policy Change'],Mor_equ_OH['Morphine_equ'],color="blue")
plt.axvline(x=0,linestyle = '-.',color = 'black')
plt.xlabel("Years from Policy Change",fontsize = 12)
plt.ylabel("Morphine_equ",fontsize = 12)
plt.title("Difference in Difference Model between FL and OH",fontsize = 16)
plt.show()
all_drug = pd.concat([FL_drug,OH_drug],ignore_index = True)
#Set dummy variable to separate treatment state and control state
all_drug['D_tr'] = [1 if x == 'FL' else 0 for x in all_drug.State]
#Set dummy variable to separate post and pre
all_drug['D_post'] = [1 if x >2010 else 0 for x in all_drug.Year]
#set interaction term
all_drug['post_policy'] = all_drug['D_post']*all_drug['D_tr']
#Run regression
mod = smf.ols('Morphine_equ~D_post+D_tr+post_policy',data = all_drug)
res = mod.fit()
print(res.summary())
