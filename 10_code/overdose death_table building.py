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
print(death_2003.dtypes)
print(death_2003.iloc[0,:])
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

#error would occur when changing the data type into float -> check NA
print(sum(death_2015.Deaths.isnull()))
#there are 15 missing values in column Deaths

#chech the rows with NA
print(death_2015.loc[death_2015["Deaths"].isnull()])
#there are some information we do not need in the end of the 15 rows.

#check all the data we have
for d in df:
    print(d.loc[d["Drug/Alcohol Induced Cause Code"].isnull()])
#all data has the same 15 rows in the end. -> delete it in the next for loop

#convert Deaths into float first
death_2015.Deaths = pd.to_numeric(death_2015.Deaths, errors = "coerce")
print(death_2015.Deaths.dtypes)

print(death_2015.loc[death_2015["Deaths"].isnull()])


count = 0
#cleaning all dataframe
for d in df:
    #delete the last 15 rows from each dataframe
    d = d.iloc[:-15,:]
    #delete the rows that the Deaths column has NA. (for 2015)
    d = d.loc[d["Deaths"].notnull()]
    #delete rows that are not record the data about death number caused by "drug"
    d = d.loc[ d["Drug/Alcohol Induced Cause Code"].str.contains("D") ]
    #delete the state name from County column and create another column to store the state name.
    county_state = d["County"].str.split(", ", n=1, expand = True)
    d["State"] = county_state[1]
    d["County"] = county_state[0]
    #delete unnecessary columns
    d.drop(["Notes","County Code","Year Code","Drug/Alcohol Induced Cause"], axis = 1, inplace = True)
    #convert float into int

    ####check NA valuse first
    #d.Year = d.Year.astype("int")
    #d.Deaths = d.Deaths.astype("int")

    print(d.head(1))

    #make a copy to avoid viewing problem in python....
    df[count]  = d.copy()

    #sum up the death number caused by drug overdose. reference: https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
    df[count] = df[count].groupby(["State","County","Year"], as_index = False).sum()
    count += 1
    ####the following do not work. but they are not necessary.
    #change data type of "Drug/Alcohol Induced Cause Code " from object to str
    #d["Drug/Alcohol Induced Cause Code"] = d["Drug/Alcohol Induced Cause Code"].to_string()
    #d.Year.astype("int32")
    #d.Deaths.astype("int32")
    
#merge all the dataframe into one table
table = pd.concat(df)
table = table.reset_index()
print(table)

table.to_csv(r'/Users/yu/Documents/Duke/courses/19fall/IDS690.02 python/mid-semester project/estimating-impact-of-opioid-prescription-regulations-team-4/20_intermediate_files/overdose_deaths.csv',header = True, index = None)
