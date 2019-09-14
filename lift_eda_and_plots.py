import pandas as pd
import plotly

'''Load data from CSV'''
df = pd.read_csv(
    '/Users/derricklewis/Documents/Flatiron/bluecore/lift_analysis/lift_analysis_assignment.csv')

''' initial look at the data'''
df.describe()

df.info()
''' 
df.info() shows that the total column is not an integer. With 
investigation there are totals that are "Missing". For our first
questions of conversion, I will choose to include these users in the 
lift conversions, but will need to clean this later when looking at
total sales 
'''

df.head()

len(df)

columns = df.columns

for i in columns:
    print('\n', df[i].nunique())
for i in columns:
    print('\n', df[i].unique())

df.loc[df.event_type == 'halted'].count()
df.loc[df.event_type == 'delivered'].count()
df.loc[df.event_type == 'purchase'].count()

"""Looking at one users journey"""
one_user = df.loc[df.email == 6024938649550848].copy()


purchases = df.loc[df.event_type == 'purchase'].copy()
converted = df[df.email.isin(list(purchases.email))].copy()


'''Maybe one hot encode the event type?'''

""" 
Need to look for 5 day window to determine purchase conversion rate
Using pandas.to_datetime to clean event_date column 
"""

df.event_date = pd.to_datetime(df.event_date, format="%Y-%m-%d")
df.event_date = df.event_date.dt.round("D")
