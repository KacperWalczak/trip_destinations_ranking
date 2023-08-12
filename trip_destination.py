import requests
from bs4 import BeautifulSoup
import pandas as pd

# Reading Countries GDP
res = requests.get('https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata_wed%C5%82ug_PKB_nominalnego_per_capita')
soup = BeautifulSoup(res.text, 'html.parser')
tables = soup.select('.wikitable')
wiki_df = pd.read_html(str(tables))[0]
# Reading User Preferences / Score of Countries
user_df = pd.read_csv('user_ranking.csv', encoding="UTF-8")
# Working on Data
result = pd.merge(wiki_df, user_df, 'outer', on='Państwo')
res = result.drop(result.columns[[2, 3, 4, 5, 6]], axis=1)
res['2021 r.'] = pd.to_numeric(res['2021 r.'][res['2021 r.'] != 'b.d.'].str.replace(' ', '')) # Getting rid of blank space inside the number
maximum_PKB = res['2021 r.'].max()
res = res.dropna()
res['Rate_PKB'] = abs(res['2021 r.'] / maximum_PKB - 1) * 5      # normalizing reversing point so the cheapest countries get the most points
res['Rate_AVG'] = (res['Rate_1'] + res['Rate_2'])/2      # average points from users
res['Rate_SUM'] = res['Rate_PKB'] + res['Rate_AVG']
res = res.sort_values(by=['Rate_SUM'], ascending=False)
res = res.reset_index()
res = res.drop(['Poz.', 'index'], axis=1)

print(maximum_PKB)
print(res.head(10))
res.to_csv('result.csv')
print(res.tail(20))




