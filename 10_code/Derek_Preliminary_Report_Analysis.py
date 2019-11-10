#!/usr/bin/env python
# coding: utf-8

# # IDS 690 - Practical Data Science
#
# ### Instructor: Dr. Nick Eubank
#
# ### Student: Derek Wales
#
# ## Mid Semester Report Preliminary analysis

# In[1]:

### Added additional line


import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols
import pyarrow
import pyarrow.parquet
import patsy
from plotnine import *
import math
import warnings
warnings.filterwarnings('ignore', module='plotnine')


# ## Endstate:
# ### Analyzing overdose deaths in Florida (Policy change in 2010) and Georgia and Alabama (No policy change)

# In[2]:


complete_df = pd.read_csv('C:\\Users\\derek\\Desktop\\MIDS 1st Semester\\Practical Data Science\\_Projects\Project One\\estimating-impact-of-opioid-prescription-regulations-team-4\\20_intermediate_files\\ultimate_final_frame_v2.csv')


# In[3]:


complete_df.head()


# In[4]:


# Can possibly give another state as a control
complete_df['State'].unique()


# ### Questions
# #### 1) Volume of Opioids Rx
# #### 2) Drug overdose deaths
# #### Doing a Pre/Post and Dif/Dif analysis

# ### Starting by
# #### Building dataframe with only FL, and then doing pre and post on opiod deaths

# In[5]:


complete_df.head()


# In[6]:


florida_df = complete_df.loc[complete_df['State']=='FL']
florida_df.describe()


# In[7]:


florida_df['Year_Changed'].unique()


# In[8]:


florida_df['Year_Changed'] = 2010
del florida_df['Unnamed: 0']
florida_df.head()


# #### Plan - Plot opiod deaths per capita pre 2010 and after 2010
# #### Use a groupby to get total deaths per year and plot

# In[9]:


florida_df['Year'].unique()


# In[10]:


florida_df_grouped = florida_df.groupby(['Year', 'FIPS', 'County', 'State','Deaths_PC'], as_index = False)
florida_df_grouped1 = florida_df_grouped.sum()
florida_df_grouped1.head()


# In[11]:


florida_df_grouped1.sample(10)


# In[12]:


# Distribution of deaths per capita
(ggplot(florida_df_grouped1,aes('Deaths_PC')) + geom_histogram()
)


# In[13]:


(ggplot(florida_df_grouped1, aes(x='Year', y= 'Deaths_PC')) +
        geom_point(color = 'cornflowerblue') + geom_smooth(method = 'lowess') +  geom_vline(xintercept=2009.9, color = 'red') + ylab('Deaths Per Capita') + ggtitle('Opiod Deaths Per Capita Florida')
)


# #### Suggests a downward trend, building a linear model to confirm.

# In[14]:


# Created a Policy Change Variable
florida_df_grouped1['Policy_Change'] = [1 if x >= 2010 else 0 for x in florida_df_grouped1['Year']]
florida_df_grouped1.sample(10)


# In[15]:


florida_df_grouped1['Year'].unique()


# In[16]:


florida_model_df = florida_df_grouped1
del florida_model_df['Year_Changed']


# In[17]:


florida_model_df = florida_model_df.rename(columns={'Policy Change':'Policy_Change'})
florida_model_df.head()


# ### Building the Pre/Post Model

# In[18]:


# Leaving all of the countys in, this does not have a Deaths/Policy Change Interaction

pre_post_model = smf.ols('Deaths_PC ~ C(Year) + C(County) + Policy_Change + Morphine_equ + Population', data = florida_model_df).fit()
print(pre_post_model.summary())


# ### Included Policy Change Interaction Term

# In[19]:


# Leaving all of the countys in (Model Validation?) Need to ask some clairifying questions
# Deaths_PC*Policy_Change
pre_post_model2 = smf.ols('Deaths_PC ~ C(Year) + C(County) + Policy_Change + Morphine_equ + C(Year):Policy_Change', data = florida_model_df).fit()
print(pre_post_model2.summary())


# #### Model interpretation: There is a no negative sign on the policy change/when it took effect. In fact it almost looks like the slope of the line in Florida went down almost entirely because of whatever happened in 2012.

# ### Building the Difference and Difference Model (EDA First)

# In[20]:


complete_df_1 = complete_df
del complete_df_1['Unnamed: 0']
complete_df_1.head()


# In[21]:


complete_df_1['State'].unique()


# In[22]:


ga_al_df = complete_df_1.loc[(complete_df_1['State'] == 'AL')|
                            (complete_df_1['State'] == 'GA')]
ga_al_df.head()


# In[23]:


ga_al_df['State'].unique()


# In[24]:


#Plot the two states together, then see if you can make some inferences
ga_al_df.head()


# In[25]:


ga_al_grouped = ga_al_df.groupby(['Year', 'FIPS', 'County', 'State','Deaths_PC'], as_index = False)
ga_al_grouped1 = ga_al_grouped.sum()
ga_al_grouped1.head()


# In[26]:


# Histogram of AL/GA
(ggplot(ga_al_grouped1,aes('Deaths_PC')) + geom_histogram()
)


# ### Plot with AL/GA w/Trendline from FL

# In[27]:


(ggplot(ga_al_grouped1, aes(x='Year', y= 'Deaths_PC')) +
        geom_point(color = 'cornflowerblue') + geom_smooth(method = 'lowess') + ylab('Deaths Per Capita') + ggtitle('Plot of Per Capita Opiod Deaths AL/GA (Black) FL (Blue)') +
        geom_smooth(data=florida_model_df, method='lowess', color ='blue', se=False)
)


# ### Plot seems to suggest that FL, AL, and GA were all going up and something in Florida around the year 2010 did have an effect

# ### Doing difference and difference analysis
# #### Plan put GA/FL/AL into one DF, and have an indicator variable for the year and whether or not the policy change took place

# In[28]:


complete_df_1['State'].unique()


# In[29]:


fl_ga_al_df = complete_df_1.loc[(complete_df_1['State'] == 'AL')|
                             (complete_df_1['State'] == 'GA')|
                             (complete_df_1['State'] == 'FL')]
fl_ga_al_df.head()


# In[30]:


fl_ga_al_df['Policy_Change'] = np.nan
fl_ga_al_df.head()


# In[31]:


fl_ga_al_df['Policy_Change'] = [1 if x == 'FL' else 0 for x in fl_ga_al_df['State']]
fl_ga_al_df.sample(10)


# In[32]:


fl_ga_al_df['Policy_Change'] = [1 if x > 2009 else 0 for x in fl_ga_al_df['Year']]


# In[33]:


fl_ga_al_df.head(5)


# #### Dataframe with FL, AL, and GA wtih the correct state and policy change labeled
# #### Going to use this for the dif/dif model discussed in class

# In[34]:


ols = smf.ols('Deaths_PC ~ C(Policy_Change) * C(Year) + State + Morphine_equ', fl_ga_al_df).fit()
ols.summary()


# ### It didn't flip the sign, in 2010 but it looks like 2012 it did. I think that the policy probably takes about 2years to start seeing the effects.

# In[ ]:
