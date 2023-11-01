#!/usr/bin/env python
# coding: utf-8

# # Project Scope 

# ### Project Scope and Plan
# 
# In July 2019, the Department for Transport released data on the type and number of journeys within
# the United Kingdom per year. The annual numbers of car journeys consistently climbed from 2015 to
# 2018, where it reached a nine-year high of 986 trips per household per year [1]. A noteworthy 75% of
# UK residents aged 17 and above possessed driver's licences, while 76% of households owned a
# minimum of one car, and 77% of the total distance travelled each year was by car.
# 
# The growing congestion resulting from these statistics prompted a need for considering alternative
# transportation methods . As a result, the Mayor of London and the London Assembly introduced
# the Mayor's Transport Strategy in 2018, focusing on three primary objectives:
# 
# - Promoting Healthy Streets & Healthy People
# - Enhancing the Public Transport Experience
# - Developing New Homes and Jobs

# ### Objectives
# 
# #### How can we increase the uptake of cycling in London?
# - Expanding cycling infrastructure so residents live within 400m of the cycling networks will increase the number of journeys completed by bike
# - Separating bike lanes from main roads, cars and large vehicles will make cyclists feel safer and thus increase the numbers of journeys completed by bike
# - Having a sustainable availability and distribution of safe and affordable hire bikes in London will increase the numbers of journeys completed by bike
# 
# #### What are the main factors that determine whether people choose to cycle?
# - More journeys are completed by bike in dry weather than rain
# - More journeys are completed by bike in the summer months than in the winter months
# - The time of day has an impact on the number of journeys completed by bike
# - More journeys are completed by bike in central London than outer London as journeys are typically shorter
# 
# #### What are the demographics of cyclists in these cities, and are there any underrepresentedgroups that can be engaged with to increase the uptake of cycling as a mode of transport?
# - The majority of journeys completed by bike in London are completed within commuting hours
# - Residents of ‘deprived’ areas of London complete fewer journeys on bike than those in ‘wealthy’ areas
# 
# #### What interventions and changes to the transport network have had the most impact on cycling engagement?

# ## 1. Prepare the Workstation

# In[2087]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install matplotlib seaborn')
get_ipython().system('pip install conda')
get_ipython().system('pip install openpyxl')


# In[2088]:


# Imports 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2089]:


# Load the data
central_london = pd.read_csv('Central London.csv')
inner_london = pd.read_csv('Inner London.csv')
outer_london = pd.read_csv('Outer London.csv')
biking_sites = pd.read_excel('Biking sites.xlsx')


# ## 2. Data Cleaning & Exploration

# # Biking Sites

# In[2090]:


# view the data
biking_sites.head()


# ### Sense Check 

# In[2091]:


# Determine the metadata of the data sets
print(biking_sites.shape)
print(biking_sites.columns)


# In[2092]:


biking_sites.info()


# In[2093]:


# Missing Values for biking sites
missing_values_biking_sites = biking_sites.isnull().sum()

# Displaying the columns with missing values and their count
missing_values_biking_sites


# #### Investigate missing values

# In[2094]:


rows_missing_biking_sites = biking_sites[biking_sites['Functional cycling area'].isnull()]
rows_missing_biking_sites


# In[2095]:


#Check: if corresponding functional cycling is in the data
richmond_data = biking_sites[biking_sites['Location'].str.contains('A307 Kew Road') & (biking_sites['Borough'] == 'Richmond upon Thames')]
richmond_data


# In[2096]:


#Replace NA
biking_sites['Functional cycling area'].fillna('unknown', inplace=True)


# In[2175]:


cleaned_bike_sites = biking_sites.copy()


# In[2176]:


cleaned_bike_sites.to_csv('cleaned_bike_sites.csv', index=False)


# # Outer London

# In[2098]:


outer_london.head(3)


# ### Sense Check

# In[2099]:


# Determine the metadata of the data sets
print(outer_london.shape)
print(outer_london.columns)


# In[2100]:


outer_london.info()


# In[2101]:


cleaned_outer_london = outer_london.copy()


# ### Survey date 

# In[2102]:


#Empty lists 
outer_lon_day_of_week = []
outer_lon_date = []


for survey_date in cleaned_outer_london['Survey date']:
    #Seperate using. split method
    if isinstance(survey_date, str):
        if ', ' in survey_date:
            day, rest = survey_date.split(', ')
            #Append corresponding to the list
            outer_lon_day_of_week.append(day)
            outer_lon_date.append(rest)
        else:
            #conditional if no value
            outer_lon_day_of_week.append('Unknown')  
            outer_lon_date.append('Unknown')  
    else:
        outer_lon_day_of_week.append('Unknown')
        outer_lon_date.append('Unknown')  

# Add new columns 'Survey_weekday' and 'Survey_date' to Cleaned London
cleaned_outer_london['Survey_weekday'] = outer_lon_day_of_week
cleaned_outer_london['Survey_date'] = outer_lon_date


# In[2103]:


outer_day_of_week_counts = cleaned_outer_london['Survey_weekday'] .value_counts()
outer_day_of_week_counts

# Rename the columns for the weekday: mapping
outer_day_mapping = {
    'lun': 'Monday',
    'mar': 'Tuesday',
    'mer': 'Wednesday',
    'jeu': 'Thursday',
    'ven': 'Friday',
    'dim': 'Saturday', 
    'sam': 'Sunday'
}
cleaned_outer_london['Survey_weekday'] = cleaned_outer_london['Survey_weekday'].replace(outer_day_mapping)


# In[2104]:


#drop original column: Survey date
cleaned_outer_london = outer_london.drop('Survey date', axis=1)


# ### Period 

# In[2105]:


#View the values within the column
outer_unique_periods = cleaned_outer_london['Period'].unique()
print(outer_unique_periods)

#Use.Split method to seperate and drop (00:00-00:00)
cleaned_outer_london['Period'] = cleaned_outer_london['Period'].str.split('(').str[0].str.strip()


# ### Zipped(Start time)

# In[2106]:


from datetime import time


#Apply datetime module 
cleaned_outer_london['Start time'] = cleaned_outer_london.apply(
    #Concatinate the start hour and minutes
    lambda row: time(row['Start hour'], row['Start minute']).strftime('%H:%M'),
    axis=1
)

cleaned_outer_london = cleaned_outer_london.drop(['Start hour','Start minute'], axis=1)


# In[2107]:


outer_column_order = [
    'Survey wave (year)',
    'Site ID',
    'Location',
    'Weather',
    'Time',
    'Period',
    'Direction',
    'Start time',
    'Number of male cycles',
    'Number of female cycles',
    'Number of unknown cycles',
    'Total cycles',
]

# Reorder the columns
cleaned_outer_london = cleaned_outer_london[outer_column_order]


# In[2108]:


cleaned_outer_london.head(1)


# In[2109]:


#Check if Period matches Time
contains_evening = cleaned_outer_london['Period'].str.contains('Early Morning')
does_not_contain = ~cleaned_outer_london['Time'].str.contains('06')

filtered_data = cleaned_outer_london[contains_evening & does_not_contain]
filtered_data

#Sidebar: Consider dropping Time from dataset.


# In[2110]:


# Missing values for outer london
missing_values_outer_london = cleaned_outer_london.isnull().sum()

# Display the columns with missing values and their count
missing_values_outer_london


# ### Weather

# In[2111]:


cleaned_outer_london['Weather'].fillna('unknown', inplace=True)


# In[2112]:


cleaned_outer_london.dtypes


# In[2113]:


cleaned_outer_london.isna().sum()


# In[2171]:


cleaned_outer_london.to_csv('cleaned_outer_london.csv', index=False)


# # Inner London

# In[2114]:


cleaned_inner_london = inner_london.copy()
cleaned_inner_london


# In[2115]:


#Drop rows with NaN
cleaned_inner_london = cleaned_inner_london.dropna(how='all', axis=0)
cleaned_inner_london


# In[2116]:


inner_duplicated_rows = cleaned_inner_london[cleaned_inner_london.index.duplicated(keep=False)]
inner_duplicated_rows.sum()


# In[2117]:


cleaned_inner_london.dtypes


# ## Year

# In[2118]:


cleaned_inner_london['Survey wave (year)'] = cleaned_inner_london['Survey wave (year)'].astype(int)


# ## Survey date

# In[2119]:


#empty lists 
inner_day_of_week = []
inner_date = []


for survey_date in cleaned_inner_london['Survey date']:
    #Seperate using. split method
    if isinstance(survey_date, str):
        if ', ' in survey_date:
            day, rest = survey_date.split(', ')
            #Append corresponding to the list
            inner_day_of_week.append(day)
            inner_date.append(rest)
        else:
            #conditional if no value
            inner_day_of_week.append('Unknown')  
            inner_date.append('Unknown')  # Set 'date' to None for non-string values
    else:
        inner_day_of_week.append('Unknown')  # Set 'day_of_week' to None for non-string values
        inner_date.append('Unknown')  # Set 'date' to None for non-string values

# Add new columns 'Survey_weekday' and 'Survey_date' to Cleaned London
cleaned_inner_london['Survey_weekday'] = inner_day_of_week
cleaned_inner_london['Survey_date'] = inner_date

# Rename the columns for the weekday: mapping
day_mapping = {
    'lun': 'Monday',
    'mar': 'Tuesday',
    'mer': 'Wednesday',
    'jeu': 'Thursday',
    'ven': 'Friday',
    'dim': 'Saturday', 
    'sam': 'Sunday'
}
cleaned_inner_london['Survey_weekday'] = cleaned_inner_london['Survey_weekday'].replace(day_mapping)

#Drop the original: Survey date
cleaned_inner_london = cleaned_inner_london.drop('Survey date', axis=1)


# # Period

# In[2120]:


inner_unique_periods = cleaned_inner_london['Period'].unique()
inner_unique_periods


# In[2121]:


#Drop the bracketed time zones
cleaned_inner_london['Period'] = cleaned_inner_london['Period'].str.split('(').str[0].str.strip()


# In[2122]:


#replace na values with "unknown"
cleaned_inner_london['Period'].fillna('unknown', inplace=True)
cleaned_inner_london.isna().sum()


# ## Time

# In[2123]:


#Replace Na with values 
cleaned_inner_london['Start hour'].fillna(0, inplace=True)
cleaned_inner_london['Start minute'].fillna(0, inplace=True)
cleaned_inner_london['Time'].fillna('unknown', inplace=True)


# In[2124]:


cleaned_inner_london.isna().sum()


# In[2125]:


cleaned_inner_london.head()


# ## Format Columns

# In[2126]:


cleaned_inner_london.dtypes


# In[2127]:


#Format all columns
cleaned_inner_london['Start hour'] = cleaned_inner_london['Start hour'].astype(int)
cleaned_inner_london['Start minute'] = cleaned_inner_london['Start minute'].astype(int)
cleaned_inner_london['Survey wave (year)'] = cleaned_inner_london['Survey wave (year)'].astype(str)
cleaned_inner_london['Number of private cycles'] = cleaned_inner_london['Number of private cycles'].astype(int)
cleaned_inner_london['Number of cycle hire bikes'] = cleaned_inner_london['Number of cycle hire bikes'].astype(int)
cleaned_inner_london['Total cycles'] = cleaned_inner_london['Total cycles'].astype(int)
cleaned_inner_london['Survey_weekday'] = cleaned_inner_london['Survey_weekday'].astype(str)
cleaned_inner_london['Survey_date'] = cleaned_inner_london['Survey_date'].astype(object)


# In[2128]:


inner_column_order = [
    'Survey wave (year)', 'Site ID', 'Location','Survey_weekday','Survey_date', 'Weather', 'Time',
       'Period', 'Direction', 'Start hour', 'Start minute',
       'Number of private cycles', 'Number of cycle hire bikes',
       'Total cycles' 
]

# Reorder the columns
cleaned_inner_london = cleaned_inner_london[inner_column_order]


# In[2129]:


cleaned_inner_london.head(1)


# ## Zipped(Start time)

# In[2130]:


from datetime import time


cleaned_inner_london['Start time'] = cleaned_inner_london.apply(
    #concatinate the hour and minutes
    lambda row: time(row['Start hour'], row['Start minute']).strftime('%H:%M'),
    axis=1
)

cleaned_inner_london = cleaned_inner_london.drop(['Start hour','Start minute'], axis=1)


# In[2131]:


inner_column_order = ['Survey wave (year)', 'Site ID', 'Location', 'Survey_weekday',
       'Survey_date', 'Weather', 'Time', 'Period', 'Direction','Start time',
       'Number of private cycles', 'Number of cycle hire bikes',
       'Total cycles']

# Reorder the columns
cleaned_inner_london = cleaned_inner_london[inner_column_order]


# In[2132]:


cleaned_inner_london.head(1)


# ### Weather

# In[2133]:


cleaned_inner_london['Weather'].fillna('unknown', inplace=True)


# In[2134]:


cleaned_inner_london.isna().sum()


# In[ ]:


cleaned_inner_london.to_csv('cleaned_inner_london.csv', index=False)


# ## Central London Cleaning

# In[2135]:


central_london.head(1)


# ####  Sense Check

# In[2136]:


# Determine the metadata of the data sets
print(central_london.shape)
print(central_london.columns)


# In[2137]:


central_london.info()


# In[2138]:


# missing values for central london
missing_values_central_london = central_london.isnull().sum()

# Display the columns within missing values and their count
missing_values_central_london


# In[2139]:


central_london.describe()


# #### Duplicate Rows | Columns

# In[2140]:


# Checking duplicates
duplicated_central = central_london.duplicated()

duplicates_central = central_london[duplicated_central] 

duplicates_central.head(5)


# In[2141]:


#Drop duplicates
cleaned_central_london = central_london.drop_duplicates()
cleaned_central_london


# In[2142]:


#Subset Unnamed Columns
cleaned_central_london = cleaned_central_london.drop(['Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16'], axis=1)


# In[2143]:


# View last row of dataset
last_row = cleaned_central_london.iloc[-1]
last_row


# In[2144]:


#drop(last row) duplicated 
cleaned_central_london = cleaned_central_london.dropna(how='all', axis=0)


# ### 'Survey date' columns 

# In[2145]:


cleaned_central_london.head(3)


# In[2146]:


#empty lists 
central_day_of_week = []
central_date = []


for survey_date in cleaned_central_london['Survey date']:
    #Seperate using. split method
    if isinstance(survey_date, str):
        if ', ' in survey_date:
            day, rest = survey_date.split(', ')
            #Append corresponding to the list
            central_day_of_week.append(day)
            central_date.append(rest)
        else:
            #conditional if no value
            central_day_of_week.append('Unknown')  
            central_date.append('Unknown')  # Set 'date' to None for non-string values
    else:
        central_day_of_week.append('Unknown')  # Set 'day_of_week' to None for non-string values
        central_date.append('Unknown')  # Set 'date' to None for non-string values

# Add new columns 'Survey_weekday' and 'Survey_date' to Cleaned London
cleaned_central_london['Survey_weekday'] = central_day_of_week
cleaned_central_london['Survey_date'] = central_date



# In[2147]:


day_of_week_counts = cleaned_central_london['Survey_weekday'] .value_counts()
day_of_week_counts


# In[2148]:


# Rename the columns for the weekday: mapping
day_mapping = {
    'lun': 'Monday',
    'mar': 'Tuesday',
    'mer': 'Wednesday',
    'jeu': 'Thursday',
    'ven': 'Friday',
    'dim': 'Saturday', 
    'sam': 'Sunday'
}
cleaned_central_london['Survey_weekday'] = cleaned_central_london['Survey_weekday'].replace(day_mapping)


# In[2149]:


#Check Unique Value
unique_weekdays = cleaned_central_london['Survey_weekday'].unique()
print(unique_weekdays)


# In[2150]:


cleaned_central_london = cleaned_central_london.drop('Survey date', axis=1)


# In[2151]:


cleaned_central_london.head(1)


# ### Format Numerical columns

# In[2152]:


missing_private_cycles = cleaned_central_london[pd.isna(cleaned_central_london['Number of private cycles'])]

missing_private_cycles


# In[2153]:


#Conditional: check if is null in No of cycles, metric matches total cycles
condition = (cleaned_central_london['Total cycles'] == 0) & (cleaned_central_london['Number of private cycles'].isna() | cleaned_central_london['Number of cycle hire bikes'].isna())

filt_rows = cleaned_central_london[condition]

# Display the filtered DataFrame
filt_rows


# ### Replace na values

# In[2154]:


cleaned_central_london['Number of private cycles'].fillna(0, inplace=True)
cleaned_central_london['Number of cycle hire bikes'].fillna(0, inplace=True)


# In[2155]:


cleaned_central_london['Number of private cycles'] = cleaned_central_london['Number of private cycles'].astype(int)
cleaned_central_london['Number of cycle hire bikes'] = cleaned_central_london['Number of cycle hire bikes'].astype(int)
cleaned_central_london['Start hour'] = cleaned_central_london['Start hour'].astype(int)
cleaned_central_london['Start minute'] = cleaned_central_london['Start minute'].astype(int)
cleaned_central_london['Total cycles'] = cleaned_central_london['Total cycles'].astype(int)


# ### Period 

# In[2156]:


#Drop unnessesary section


# In[2157]:


unique_periods = cleaned_central_london['Period'].unique()
print(unique_periods)


# In[2158]:


#Drop the bracketed tim zones
cleaned_central_london['Period'] = cleaned_central_london['Period'].str.split('(').str[0].str.strip()


# In[2159]:


#Check data for Period and Time for possible mislabelling

contains_evening = cleaned_central_london['Period'].str.contains('Early Morning')
does_not_contain = ~cleaned_central_london['Time'].str.contains('06')

filtered_data = cleaned_central_london[contains_evening & does_not_contain]
filtered_data


# In[2160]:


cleaned_central_london.dtypes


# In[2161]:


cleaned_central_london.dtypes


# ## Weather

# In[2162]:


cleaned_central_london['Weather'].fillna('unknown', inplace=True)


# In[2163]:


cleaned_central_london.isnull().sum()


# In[2164]:


cleaned_central_london.head()


# ## Zipped(start hour)

# In[2165]:


#Apply date time module

from datetime import time

cleaned_central_london['Start time'] = cleaned_central_london.apply(
    #Concatinate start hour and minute
    lambda row: time(row['Start hour'], row['Start minute']).strftime('%H:%M'),
    axis=1
)


# In[2166]:


cleaned_central_london.head(2)


# In[2167]:


cleaned_central_london = cleaned_central_london.drop(['Start hour','Start minute'], axis=1)


# In[2168]:


column_order = [
    'Survey wave (calendar quarter)',
    'Equivalent financial quarter',
    'Site ID',
    'Location',
    'Survey_date',
    'Survey_weekday',
    'Weather',
    'Time',
    'Period',
    'Direction',
    'Start time',
    'Number of private cycles',
    'Number of cycle hire bikes',
    'Total cycles',
]

# Reorder the columns
cleaned_central_london = cleaned_central_london[column_order]


# In[2169]:


cleaned_central_london.head(2)


# In[2177]:


cleaned_central_london.to_csv('cleaned_central_london.csv', index=False)


# In[ ]:




