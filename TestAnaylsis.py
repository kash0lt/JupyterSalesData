#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
from os import listdir
from os.path import isfile, join


# In[42]:


import matplotlib.pyplot as plt


# In[43]:


from itertools import combinations
from collections import Counter


# In[44]:


### merging 12 months of sales data into a single csv file


# In[45]:


onlyfiles = [f for f in listdir('./Sales_Data/')]

all_data = pd.DataFrame()

for file in onlyfiles:
    df = pd.read_csv('./Sales_data/'+file)
    all_data = pd.concat([all_data, df])
all_data.to_csv('./AllMonthsData.csv', index=False)


# In[46]:


### Read in updated data


# In[47]:


allData = pd.read_csv('./AllMonthsData.csv')


# In[48]:


### Cleanup the data
### rows with NaN values and Empty Data


# In[49]:


allData = allData.dropna(axis=0, how='all')


# In[50]:


allData = allData[allData['Order Date'].str[0:2] != 'Or']


# In[51]:


### Convert columns to correct data type Qty, Price, OrderDate


# In[52]:


allData['Quantity Ordered'] = pd.to_numeric(allData['Quantity Ordered'])
allData['Price Each'] = pd.to_numeric(allData['Price Each'])
allData['Order Date'] = pd.to_datetime(allData['Order Date'])


# In[53]:


### Augment data with some additional columns
## Add Month column


# In[54]:


allData['Month'] = allData['Order Date'].dt.month

allData['Hour'] = allData['Order Date'].dt.hour
allData['Minute'] = allData['Order Date'].dt.minute
allData['Count'] = 1
allData.head()


# In[55]:


### Add a salestotal column for qty * price in the dataframe


# In[56]:


allData['SalesTotal'] = allData['Quantity Ordered'] * allData['Price Each']


# In[57]:


#### Separate out the city (ST)


# In[58]:


#### use the dot apply method from pandas with a format string


# In[59]:


def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

allData['City'] = allData['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")


# In[60]:


results = allData.groupby('Month').sum()


# In[61]:


months = range(1,13)
plt.bar(months, results['SalesTotal'])
plt.xticks(months)
plt.ylabel('Sales in US $')
plt.xlabel('Months')
plt.show()


# In[62]:


#### What US city had the highest number of sales
results = allData.groupby('City').sum()


# In[63]:


## This groups unique citys into a list of City names in same order as results table
cities = [city for city, df in allData.groupby('City')]

plt.bar(cities, results['SalesTotal'])
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('Sales in US $')
plt.xlabel('City Name')
plt.show()


# In[64]:


hours = [hour for hour, df in allData.groupby('Hour')]

plt.plot(hours, allData.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Num of Orders')
plt.grid()

plt.show()


# In[69]:


### Let's get a new dataframe with JUST the rows that are duplicate by order ID
## duplicated(keep=False) keeps ALL duplcated rows, not just the first or last
df = allData[allData['Order ID'].duplicated(keep=False)]
df = df.copy()   ## This makes df an actual memory copy and not a view anymore
df.drop(['Hour', 'Minute', 'City'], axis=1, inplace=True)
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
## Now drop the duplicates by order id
df = df[['Order ID', 'Grouped', 'Count']].drop_duplicates()


# In[70]:


count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
count.most_common(10)
for key, value in count.most_common(15):
    print(key, value)


# In[73]:


df = allData.groupby('Product')

quantity_ordered = df.sum()['Quantity Ordered']
products = [product for product, dataframe in df]


# In[77]:


plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=8)
plt.ylabel('Quantity')
plt.xlabel('Products')
plt.show()


# In[81]:


prices = allData.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Products')
ax1.set_ylabel('Quantity', color='g')
ax2.set_ylabel('Price', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()


# In[ ]:




