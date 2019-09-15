import pandas as pd
import plotly
import datetime

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

""" 
Need to look for 5 day window to determine purchase conversion rate
Using pandas.to_datetime to clean event_date column 
"""

df.event_date = pd.to_datetime(df.event_date, format="%Y-%m-%d")
df.event_date = df.event_date.dt.round("D")


"""Looking at one users journey"""
one_user = df.loc[df.email == 5312915884212224].copy()


'''Maybe one hot encode the event type?'''

""" 
Start with a list of delivered and a list of halted.
Take a count of each list
Gather email from those. Match emails to purchased and add.
Filter purchases frome within 5 days of email
count purchases that meet the criteria
Divide by total purchases and control.  
"""

big_bc_list = df.loc[df.event_type == 'delivered'].copy()
big_bc_list.email.nunique()  # 506406

big_control_list = df.loc[df.event_type == 'halted'].copy()
big_control_list.email.nunique()  # 28596

bc = df[(df.email.isin(list(big_bc_list.email))) &
        (df.event_type == 'purchase')].copy()
bc['converted'] = 0
control = df[(df.email.isin(list(big_control_list.email)))
             & (df.event_type == 'purchase')].copy()
control['converted'] = 0


# not pretty. not fast.

def converted(emails, purchases, type):
    '''
    Dates are a challenge. Function takes two lists and type of email 
    Start with each purchased date and validate an email delivery date 
    is less than or equal than 5 days.
    append the purchased list with a 1 to mark that this purchase was converted 
    from an email (or control) 
    '''

    for i in range(len(purchases)):
        print(i)
        test = False  # reset test to false

        delivered_dates = emails.event_date.loc[(
            emails.event_type == type) & (emails.email == purchases.email.iloc[i])]
        # Gather all the email delivered dates from the person who purchased

        for _ in range(len(delivered_dates)):
            if test is False:
                test = purchases.iloc[i]['event_date'] - \
                    delivered_dates.iloc[_] <= datetime.timedelta(days=5) and \
                    purchases.iloc[i]['event_date'] - \
                    delivered_dates.iloc[_] > datetime.timedelta(days=0)
                # Test to see if there is an email within 5 days before purchasing
            else:
                purchases['converted'].iloc[i] = 1


converted(big_bc_list, bc, 'delivered')

converted(big_control_list, control, 'halted')


'''Do two purchases by the same person count as being converted twice?'''

bc['converted'].sum()
control['converted'].sum()
