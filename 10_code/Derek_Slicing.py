import pandas as pd
import numpy as np

df = pd.read_csv("pop_counties_20062012.csv")

### Columns Needed - BUYER_STATE, BUYER_COUNTY, countyfips, year, population

required_states_df = df.loc[:, ['BUYER_STATE', 'BUYER_COUNTY', 'countyfips', 'year', 'population']]
required_states_df.head()

required_states_df = required_states_df.loc[((required_states_df['BUYER_STATE'] == 'TX')|
                                             (required_states_df['BUYER_STATE'] == 'WA')|
                                             (required_states_df['BUYER_STATE'] == 'FL')|
                                             (required_states_df['BUYER_STATE'] == 'GA')|
                                             (required_states_df['BUYER_STATE'] == 'OR')|
                                             (required_states_df['BUYER_STATE'] == 'CA'))]



required_states_v2 = required_states_df.rename(columns={'BUYER_STATE':'State', 'BUYER_COUNTY':'County', 'countyfips':'FIPS', 'year':'Year', 'population': 'Population'})
required_states_v2.head()

required_states_v2.to_excel('States_Updated_DF.xlsx') #passed initial excel sanity check. 

required_states_v2.to_csv('Counties_DF_Merge_Ready.csv') #passed initial excel sanity check. 