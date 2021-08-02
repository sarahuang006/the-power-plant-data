#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

df_entso = pd.read_csv("../data/entso.csv")
df_gppd = pd.read_csv("../data/gppd.csv")
df_platts = pd.read_csv("../data/platts.csv")


# In[2]:


# drop missing value of platts_plant_id
df_gppd = pd.DataFrame(df_gppd[df_gppd['platts_plant_id'].notna()])
df_platts = pd.DataFrame(df_platts[df_platts['platts_plant_id'].notna()])


# In[3]:


# merge gppd and platts data based on shared platts_plant_id column
df_gppd['platts_plant_id']=df_gppd['platts_plant_id'].astype(str)
df_platts['platts_plant_id']=df_platts['platts_plant_id'].astype(str)

df_gppd_platts = df_gppd.merge(df_platts, how='inner', on=['platts_plant_id'])


# In[4]:


# compare merged gppd_platts dataframe with entso dataset accounding to the plant name, plant_name_x and plant_name_y are
# from gppd and platts datasets, if plants name in entso equare to either of them, it is the same plant

#precoss the plant_name to lowercase for comparison
df_entso['plant_name'] = df_entso['plant_name'].str.lower()
df_gppd_platts['plant_name_x'] = df_gppd_platts['plant_name_x'].str.lower()
df_gppd_platts['plant_name_y'] = df_gppd_platts['plant_name_y'].str.lower()

#process entso dataframe's country name, removed short form in parenthesis
df_entso['country'] = df_entso['country'].str.replace(r"\(.*\)", "")


df_entso_combined_y = df_entso.merge(df_gppd_platts, left_on='plant_name', right_on = 'plant_name_y',how='inner')
df_entso_combined_x = df_entso.merge(df_gppd_platts, left_on='plant_name', right_on = 'plant_name_x',how='inner')



# In[5]:


# remove duplicats in merged data
df_entso_combined_x = df_entso_combined_x.drop_duplicates(subset='entso_unit_id', keep="last")
df_entso_combined_y = df_entso_combined_y.drop_duplicates(subset='entso_unit_id', keep="last")


# In[6]:



# combine results

df_entso_combined_x = df_entso_combined_x.append(df_entso_combined_y)


# In[9]:


mapping = df_entso_combined_x[['entso_unit_id', 'platts_plant_id', 'gppd_plant_id']]


# In[13]:


mapping.to_csv('mapping.csv', index=False)

