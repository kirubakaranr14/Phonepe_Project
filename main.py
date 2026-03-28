import os
import json
import pandas as pd


#  Aggregated_Insurance :

ins_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/aggregated/insurance/country/india/state/'
Agg_ins_state_list = os.listdir(ins_path)
Agg_ins_state_list

ins_data = {'State': [], 'Year': [], 'Quater': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}

for i in Agg_ins_state_list:
  p_i = ins_path + i + '/'
  Agg_ins_year = os.listdir(p_i)         ##'/content/pulse/data/aggregated/insurance/country/india/state/'

  for j in Agg_ins_year:
    p_j = p_i + j + '/'
    Agg_ins_year_list = os.listdir(p_j)  ##'/content/pulse/data/aggregated/insurance/country/india/state/any_state/'

    for k in Agg_ins_year_list:
      p_k = p_j + k                      ##'/content/pulse/data/aggregated/insurance/country/india/state/any_state/1.json'

      Data = open(p_k,'r')
      D = json.load(Data)

      for z in D['data']['transactionData']:
        name = z['name']
        count = z['paymentInstruments'][0]['count']
        amount = z['paymentInstruments'][0]['amount']

        ins_data['Transaction_type'].append(name)
        ins_data['Transaction_count'].append(count)
        ins_data['Transaction_amount'].append(amount)
        ins_data['State'].append(i)
        ins_data['Year'].append(j)
        ins_data['Quater'].append(int(k.strip('.json')))

Agg_ins = pd.DataFrame(ins_data)
Agg_ins.to_sql('aggregated_insurance', engine, if_exists='replace', index=False)
Agg_ins


# Aggregated_Transaction :

path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/aggregated/transaction/country/india/state/'
Agg_trans_state = os.listdir(path)
Agg_trans_state

trans_data = { 'State': [], 'Year': [], 'Quater': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': [] }

for i in Agg_trans_state:
    p_i = path + i + "/"      #["/content/pulse/data/aggregated/transaction/country/india/state/any_state"]
    Agg_trans_yr = os.listdir(p_i)

for j in Agg_trans_yr:
        p_j = p_i + j + "/"   #["/content/pulse/data/aggregated/transaction/country/india/state/any_state/2018/"]
        Agg_yr_state_list = os.listdir(p_j)

        for k in Agg_yr_state_list:
          p_k = p_j + k       #["/content/pulse/data/aggregated/transaction/country/india/state/any_state/2018/1.json"]

          Data = open(p_k, 'r')
          D = json.load(Data)

          for z in D['data']['transactionData']:
            name=z['name']
            count=z['paymentInstruments'][0]['count']
            amount=z['paymentInstruments'][0]['amount']

            trans_data['Transaction_type'].append(name)
            trans_data['Transaction_count'].append(count)
            trans_data['Transaction_amount'].append(amount)
            trans_data['State'].append(i)
            trans_data['Year'].append(j)
            trans_data['Quater'].append(int(k.strip('.json')))

Agg_trans = pd.DataFrame(trans_data)
Agg_trans.to_sql('aggregated_transaction', engine, if_exists='replace', index=False)
Agg_trans


# Aggregated_User :

user_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/aggregated/user/country/india/state/'
Agg_user_state = os.listdir(user_path)
Agg_user_state

user_data = { 'State': [], 'Year': [], 'Quater': [], 'Brand': [], 'Count': [], 'Percentage': [] }

for i in Agg_user_state:
  p_i = user_path + i + "/"
  Agg_user_state_list = os.listdir(p_i)

  for j in Agg_user_state_list:
    p_j = p_i + j + "/"
    Agg_user_year_list = os.listdir(p_j)

    for k in Agg_user_year_list:
      p_k = p_j + k

      Data = open(p_k, 'r')
      D = json.load(Data)

      if D['data']['usersByDevice'] is not None: ## Sometimes phonepe dataset may not have data in .json file, python consider that "UserbyDevice = NULL"
                                                 ## make sure to write condition whether .json is Null before entering into loop..!
        for z in D['data']['usersByDevice']:
          brand = z['brand']
          count = z['count']
          percentage = z['percentage']

          user_data['Brand'].append(brand)
          user_data['Count'].append(count)
          user_data['Percentage'].append(percentage)
          user_data['State'].append(i)
          user_data['Year'].append(j)
          user_data['Quater'].append(int(k.strip('.json')))

Agg_user = pd.DataFrame(user_data)
Agg_user.to_sql('aggregated_user', engine, if_exists='replace', index=False)
Agg_user


# Map_Insurance :

map_ins_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/map/insurance/hover/country/india/state/'
map_ins_state = os.listdir(map_ins_path)
map_ins_state

map_ins_data = {'State': [], 'Year': [], 'Quater': [], 'District': [], 'Count': [], 'Amount': []}

for i in map_ins_state:
    p_i = map_ins_path + i + '/'
    Map_ins_yr = os.listdir(p_i)

    for j in Map_ins_yr:
        p_j = p_i + j + '/'
        Map_ins_yr_list = os.listdir(p_j)

        for k in Map_ins_yr_list:
            p_k = p_j + k

            Data = open(p_k, 'r')
            D = json.load(Data)

            for z in D['data']['hoverDataList']:
              name = z['name']
              count = z['metric'][0]['count']
              amount = z['metric'][0]['amount']

              map_ins_data['State'].append(i)
              map_ins_data['Year'].append(j)
              map_ins_data['Quater'].append(int(k.strip('.json')))

              map_ins_data['District'].append('name')
              map_ins_data['Count'].append('count')
              map_ins_data['Amount'].append('amount')

map_ins = pd.DataFrame(map_ins_data)
map_ins.to_sql('map_insurance', engine, if_exists='replace', index=False)
map_ins


# Map_Transaction :

map_trans = '/Users/karan/Desktop/PhonePe_Project/pulse/data/map/transaction/hover/country/india/state/'
map_trans_state = os.listdir(map_trans)
map_trans_state

map_trans_data = {'state':[], 'year':[], 'quater':[], 'district':[], 'count':[], 'amount':[]}

for i in map_trans_state:
  p_i = map_trans + i + '/'
  map_trans_state_list = os.listdir(p_i)

  for j in map_trans_state_list:
    p_j = p_i + j + '/'
    map_trans_year_list = os.listdir(p_j)

    for k in map_trans_year_list:
      p_k = p_j + k

      Data = open(p_k, 'r')
      D = json.load(Data)

      for z in D['data']['hoverDataList']:
        name = z['name']
        count = z['metric'][0]['count']
        amount = z['metric'][0]['amount']

        map_trans_data['state'].append(i)
        map_trans_data['year'].append(j)
        map_trans_data['quater'].append(int(k.strip('.json')))

        map_trans_data['district'].append(name)
        map_trans_data['count'].append(count)
        map_trans_data['amount'].append(amount)

map_trans_list = pd.DataFrame(map_trans_data)
map_trans_list.to_sql('map_transaction', engine, if_exists='replace', index=False)
map_trans_list


# Map_User :

# 1. Path to map user :
map_user_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/map/user/hover/country/india/state/'
map_user_state = os.listdir(map_user_path)
map_user_state

# 2. Initialize dictionary :
map_user = {'state': [], 'year': [], 'quater': [], 'district': [], 'registeredUsers': [], 'appOpens': []}

#3. for loop :
for i in map_user_state:
  p_i = map_user_path + i + '/'
  map_user_state_list = os.listdir(p_i)

  for j in map_user_state_list:
    p_j = p_i + j + '/'
    map_user_year_list = os.listdir(p_j)

    for k in map_user_year_list:
      p_k = p_j + k

      Data = open(p_k, 'r')
      D = json.load(Data)

      if D['data']['hoverData'] is not None:
        for z in D['data']['hoverData'].items():
          map_user['state'].append(i)
          map_user['year'].append(j)
          map_user['quater'].append(int(k.strip('.json')))
          district = z[0]
          values = z[1]
          map_user['district'].append(district)
          map_user['registeredUsers'].append(values['registeredUsers'])
          map_user['appOpens'].append(values['appOpens'])

#4. Create the DataFrame:
df_map_user = pd.DataFrame(map_user)
df_map_user.to_sql('Map_user', engine, if_exists='replace', index=False)
df_map_user


# Top_Insurance :

top_ins_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/top/insurance/country/india/state/'
top_ins_state = os.listdir(top_ins_path)

top_ins_data = {'state': [], 'year': [], 'quater': [], 'districts': [], 'count': [], 'amount':[]}

for i in top_ins_state:
  p_i = top_ins_path + i + '/'
  top_ins_state_list = os.listdir(p_i)

  for j in top_ins_state_list:
    p_j = p_i + j + '/'
    top_user_year_list = os.listdir(p_j)

    for k in top_user_year_list:
      p_k = p_j + k

      Data = open(p_k, 'r')
      D = json.load(Data)


      for z in D['data']['districts']:

        enitityName = z['entityName']
        count = z['metric']['count']
        amount = z['metric']['amount']

        top_ins_data['state'].append(i)
        top_ins_data['year'].append(j)
        top_ins_data['quater'].append(int(k.strip('.json')))
        top_ins_data['districts'].append(enitityName)
        top_ins_data['count'].append(count)
        top_ins_data['amount'].append(amount)

top_ins_list = pd.DataFrame(top_ins_data)
top_ins_list.to_sql('top_insurance', engine, if_exists='replace', index=False)
top_ins_list


#Top_Transactions :

top_trans_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/top/transaction/country/india/state/'
top_trans_state = os.listdir(top_trans_path)
top_trans_state

top_trans_user = {'state': [], 'year': [], 'quater': [], 'districts': [], 'count': [], 'amount':[]}

for i in top_trans_state:
  p_i = top_trans_path + i + '/'
  top_trans_state_list = os.listdir(p_i)

  for j in top_trans_state_list:
    p_j = p_i + j + '/'
    top_trans_year_list = os.listdir(p_j)

    for k in top_trans_year_list:
      p_k = p_j + k

      Data = open(p_k, 'r')
      D = json.load(Data)

      for z in D['data']['districts']:

        enitityName = z['entityName']
        count = z['metric']['count']
        amount = z['metric']['amount']

        top_trans_user['state'].append(i)
        top_trans_user['year'].append(j)
        top_trans_user['quater'].append(int(k.strip('.json')))
        top_trans_user['districts'].append(enitityName)
        top_trans_user['count'].append(count)
        top_trans_user['amount'].append(amount)

top_trans_list = pd.DataFrame(top_trans_user)
top_trans_list.to_sql('top_transaction', engine, if_exists='replace', index=False)
top_trans_list


#Top_User :

top_user_path = '/Users/karan/Desktop/PhonePe_Project/pulse/data/top/user/country/india/state/'
top_user_state = os.listdir(top_user_path)
top_user_state

top_user_data = {'state': [], 'year': [], 'quater': [], 'districts': [], 'registeredUsers': []}

for i in top_user_state:
  p_i = top_user_path + i + '/'
  top_user_state_list = os.listdir(p_i)
  
  for j in top_user_state_list:
    p_j = p_i + j + '/'
    top_user_year_list = os.listdir(p_j)

    for k in top_user_year_list:
      p_k = p_j + k

      Data = open(p_k, 'r')
      D = json.load(Data)
        
      for z in D['data']['districts']:
        name = z['name']
        registeredUsers = z['registeredUsers']
        
        top_user_data['state'].append(i)
        top_user_data['year'].append(j)
        top_user_data['quater'].append(int(k.strip('.json')))
        top_user_data['districts'].append(name)
        top_user_data['registeredUsers'].append(registeredUsers)

top_user_list = pd.DataFrame(top_user_data)
top_user_list.to_sql('aggregated_transaction', engine, if_exists='replace', index=False)
top_user_list




# Push the Map User data you just finished
#df_map_user.to_sql('map_user_table', engine, if_exists='replace', index=False)

#print("Success! Map User data is in pgAdmin.")