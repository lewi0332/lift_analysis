import pandas as pd
import datetime

'''Load data from CSV'''
df = pd.read_csv(
    '/Users/derricklewis/Documents/Flatiron/bluecore/lift_analysis/lift_analysis_assignment.csv')


''' initial look at the data'''
df.head()
df.describe()

df.info()
'''
df.info() shows that the total column is not an integer. With
investigation there are totals that are "MISSING". For our first
questions of conversion, I will choose to include these rows in the
lift conversions, but will need to clean this later when looking at
total revenue
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
# df.event_date = df.event_date.dt.round("D")


"""Looking at one users journey"""
user_one = df.loc[df.email == 5312915884212224].copy()
user_two = df.loc[df.email == 5994933019213824].copy()
user_three = df.loc[df.email == 5312915884212224].copy()

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
big_bc_list['converted'] = 0

big_control_list = df.loc[df.event_type == 'halted'].copy()
big_control_list.email.nunique()  # 28596
big_control_list['converted'] = 0

bc = df[(df.email.isin(list(big_bc_list.email))) &
        (df.event_type == 'purchase')].copy()
bc['converted'] = 0
control = df[(df.email.isin(list(big_control_list.email)))
             & (df.event_type == 'purchase')].copy()
control['converted'] = 0


# not pretty. not fast.

def add_converted(emails, purchases):
    '''
    Dates were a challenge. This function inputs two lists and a cohort type
    Start with each purchased date and validate an email delivery date
    is within 5 days.
    It then appends the purchased list with a 1 to mark that this purchase was converted
    from an email
    '''

    for i in range(len(purchases)):
        print(i)
        test = False  # reset test to false

        delivered_dates = emails.event_date.loc[emails.email ==
                                                purchases.email.iloc[i]]
        # Gather all the email delivered dates from the person who purchased

        for _ in range(len(delivered_dates)):
            if test is False:
                test = purchases.iloc[i]['event_date'] - \
                    delivered_dates.iloc[_] <= datetime.timedelta(days=10) and \
                    purchases.iloc[i]['event_date'] - \
                    delivered_dates.iloc[_] > datetime.timedelta(days=0)
                # Test to see if there is an email within 5 days before purchasing
            else:
                purchases['converted'].iloc[i] = 1


'''Run the function on both the bc and control lists'''
add_converted(big_bc_list, bc)
add_converted(big_control_list, control)


def add_converted_rev(emails, purchases):
    '''
    Dates were a challenge. This function inputs two lists and a cohort type
    Start with each purchased date and validate an email delivery date
    is within 5 days.
    It then appends the purchased list with a 1 to mark that this purchase was converted
    from an email
    '''

    for i in range(len(purchases)):
        print(i)
        test = False  # reset test to false

        delivered_dates = emails.event_date.loc[emails.email ==
                                                purchases.email.iloc[i]]
        # Gather all the email delivered dates from the person who purchased

        for _ in range(len(delivered_dates)):
            if test is False:
                test = delivered_dates.iloc[_] - \
                    purchases.iloc[i]['event_date'] <= datetime.timedelta(days=10) and \
                    delivered_dates.iloc[_] - \
                    purchases.iloc[i]['event_date'] > datetime.timedelta(
                        days=0)
                # Test to see if there is an email within 5 days before purchasing
            else:
                purchases['converted'].iloc[i] = 1


'''Run the function in reverse to see email effectiveness'''
add_converted_rev(bc, big_bc_list)
add_converted_rev(control, big_control_list)


'''Do two purchases by the same person count as being converted twice?'''


'''Print results'''
# -----------------------------------------------------------------------
''' Number of converted purchases'''
bc_purchases_conversion = (bc['converted'].sum() / len(bc))
control_purchase_conversion = (
    control['converted'].sum() / len(control))
purchase_lift = ((bc_purchases_conversion - control_purchase_conversion) /
                 control_purchase_conversion)
print("Purchase Conversion rate")
print(
    f".....BC Cohort: {bc['converted'].sum()} of {len(bc)} for {bc_purchases_conversion:.2%}")
print(
    f".....Control Cohort: {control['converted'].sum()} of {len(control)} for {control_purchase_conversion:.2%}")
print(f"This created a {purchase_lift:.2%} lift in conversion")

# -----------------------------------------------------------------------
'''Number of converted customers'''
only_converted_purchases_bc = bc.loc[bc.converted == 1].copy()
only_converted_purchases_control = control.loc[control.converted == 1].copy()
bc_cust_conversion = only_converted_purchases_bc.email.nunique() / \
    big_bc_list.email.nunique()
control_cust_conversion = only_converted_purchases_control.email.nunique() / \
    big_control_list.email.nunique()
customer_lift = (bc_cust_conversion-control_cust_conversion) / \
    control_cust_conversion
print("\n\nCustomer Conversion rate")
print(f".....BC Cohort: {bc_cust_conversion:.2%}")
print(f".....Control Cohort: {control_cust_conversion:.2%}")
print(f"This created a {customer_lift:.2%} lift in conversion")

# -----------------------------------------------------------------------
''' Number of converted emails'''
bc_email_conversion = (big_bc_list['converted'].sum() / len(big_bc_list))
control_email_conversion = (
    big_control_list['converted'].sum() / len(big_control_list))
email_lift = ((bc_email_conversion - control_email_conversion) /
              control_email_conversion)
print("\n\nEmail Conversion rate")
print(
    f".....BC Cohort: {big_bc_list['converted'].sum()} of {len(big_bc_list)} for {bc_email_conversion:.2%}")
print(
    f".....Control Cohort: {big_control_list['converted'].sum()} of {len(big_control_list)} for {control_email_conversion:.2%}")
print(f"This created a {email_lift:.2%} lift in conversion")

# -----------------------------------------------------------------------
'''Revenue attributed to emails
-First remove all values named "missing" and less than 0 on both lists
'''
bc_rev = bc.loc[bc.total != 'MISSING'].copy()
control_rev = control.loc[control.total != 'MISSING'].copy()
bc_rev['total'] = bc_rev['total'].astype(float)
control_rev['total'] = control_rev['total'].astype(float)

# quick variable with both numbers
bc_bad_totals = len(bc.loc[bc.total == 'MISSING']) + \
    len(bc_rev.loc[bc_rev.total <= 0])
control_bad_totals = len(
    control.loc[control.total == 'MISSING']) + len(control_rev.loc[control_rev.total <= 0])

print('\n\nAttributed revenue per email.\n')

# new lists with only good totals

bc_totals = bc_rev.loc[bc_rev.total > 0].copy()
control_totals = control_rev.loc[control_rev.total > 0].copy()


bc_rev_per_email = bc_totals.loc[bc_totals.converted == 1].total.sum(
) / len(bc_totals.loc[bc_totals.converted == 1])
control_rev_per_email = control_totals.loc[control_totals.converted == 1].total.sum(
) / len(control_totals.loc[control_totals.converted == 1])
rev_lift = (bc_rev_per_email-control_rev_per_email)/control_rev_per_email

print(f".....BC Cohort: ${bc_rev_per_email:.2f}")
print(f".....Control Cohort: ${control_rev_per_email:.2f}")
print(f"This created a {rev_lift:.2%} lift in conversion")

print(f"\nHowever, here are {bc_bad_totals} \
purchase totals labeled 'MISSING' or less than 0 \
in the BC cohort and there are {control_bad_totals} \
purchase totals labeled 'MISSING' or less than \
0 in the Control cohort")
