import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests, zipfile, io
#import redis


html_page = urlopen("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx")
soup = BeautifulSoup(html_page)

result =  soup.find("a",{'id':'ContentPlaceHolder1_btnhylZip'})
link = result.get('href')
print(link)

#download file
r = requests.get(link, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

#extract filename
file = link.split('/')
filename = file[-1].split('_')[0] + '.csv'
print(filename)

data = pd.read_csv(filename)
equity_data = data[['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE']]
equity_data['SC_NAME'] = equity_data['SC_NAME'].apply(lambda x: x.strip().lower())

equity_data.set_index('SC_NAME', inplace = True)
equity_data_dict = equity_data.to_dict(orient='index')

import pickle
pickle.dump(equity_data_dict, open("equity_data_dict.pickle", "wb"))

# conn = redis.Redis(host='localhost', port=6379, db=0)
# for key, value in equity_data_dict.items():
# 	conn.set(key, str(value))