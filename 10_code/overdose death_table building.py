import pandas as pd
import numpy as np

#read all files
death_2003 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2003.txt", sep='\t')
death_2004 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2004.txt", sep='\t')
death_2005 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2005.txt", sep='\t')
death_2006 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2006.txt", sep='\t')
death_2007 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2007.txt", sep='\t')
death_2008 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2008.txt", sep='\t')
death_2009 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2009.txt", sep='\t')
death_2010 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2010.txt", sep='\t')
death_2011 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2011.txt", sep='\t')
death_2012 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2012.txt", sep='\t')
death_2013 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2013.txt", sep='\t')
death_2014 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2014.txt", sep='\t')
death_2015 = pd.read_table("/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/00_source/US_VitalStatistics/Underlying Cause of Death, 2015.txt", sep='\t')


#take a look at the data
print(death_2003.head())
print(death_2003.columns)
#There is no column identifies state and column "county" has two information- state and county.

#put all dataframe into a list in order to use for loop to check all dataframe easily
df = [death_2003, death_2004, death_2005, death_2006, death_2007, death_2008, death_2009, death_2010, death_2011, death_2012, death_2013, death_2014, death_2015]

#check how each file look like
for d in df:
    print(d.describe())
#each file contains different number of counties
#It seems like there is no death data in 2015

#check 2015
print(death_2015.head())
#Deaths column exists in the data but is not showed by describe function
#check data type
print(death_2015.Deaths.dtypes)
#data type is object rather than float
#change the data type into float
death_2015.Deaths = death_2015.Deaths.astype(float)
print(death_2015.Deaths.dtypes)


#delete the state name from County column and create another column to store the state name.