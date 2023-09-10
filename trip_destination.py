import requests
from bs4 import BeautifulSoup
import pandas as pd
from location import get_lat_long
from location import calculate_distance


# Reading Countries GDP
res = requests.get('https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata_wed%C5%82ug_PKB_nominalnego_per_capita')
soup = BeautifulSoup(res.text, 'html.parser')
tables = soup.select('.wikitable')
wiki_df = pd.read_html(str(tables))[0]
# Reading User Preferences / Score of Countries
user_df = pd.read_csv('countries_rating.csv', encoding="UTF-8")
# Working on Data
result = pd.merge(wiki_df, user_df, 'outer', on='Państwo')
result = result.drop(result.columns[[2, 3, 4, 5, 6]], axis=1)
result['2021 r.'] = pd.to_numeric(result['2021 r.'][result['2021 r.'] != 'b.d.'].str.replace(' ', '')) # Getting rid of blank space inside the number
maximum_PKB = result['2021 r.'].max()
result = result.dropna()
result['Rate_PKB'] = abs(result['2021 r.'] / maximum_PKB - 1) * 5      # normalizing reversing point so the cheapest countries get the most points
result['Users_rate_avg'] = (result['Rate_1'] + result['Rate_2'])/2      # average points from users


result = result.reset_index()
result = result.drop(['Poz.', 'index'], axis=1)

# managing distance from users location to capital of the country to estimate trip cost

capitals_df = pd.read_csv('capitals_df.csv', encoding="UTF-8")
result.rename(columns={"Państwo": "Country"}, inplace=True)
result = pd.merge(result, capitals_df, 'outer', on='Country')


# getting location of the user
user_coordinates = get_lat_long('https://pl.wikipedia.org/wiki/Warszawa')
# user_coordinates = user_coordinates[0] + ', ' + user_coordinates[1]
result['User_coordinates'] = user_coordinates
result['Distance'] = result.apply(lambda row: calculate_distance(row['Coordinates'], row['User_coordinates']), axis=1)

maximum_distance = result['Distance'].max()
result['Distance_rate'] = abs(result['Distance'] / maximum_distance - 1) * 5

result = result.drop(['Unnamed: 0'], axis=1)
result['Summary'] = result['Rate_PKB'] + result['Users_rate_avg'] + result['Distance_rate']
result = result.sort_values(by=['Summary'], ascending=False)
result = result.reset_index(drop=True)

print(maximum_PKB)
print(result.head(10))
result.to_csv('result.csv')
print(result.tail(20))




