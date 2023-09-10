import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.distance import geodesic


def get_capital_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="wikitable")
    rows = table.find_all("tr")
    result = []
    for row in rows[1:]:
        columns = row.find_all("td")
        country = columns[1].text.strip()
        capital = columns[4].text.strip()
        if columns[4].find("a", href=True):
            capital_link = columns[4].find("a")["href"]
        else:
            capital_link = columns[1].find("a")["href"]
        result.append([country, capital, capital_link])
    return result


def get_lat_long(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    latitude = soup.find("span", class_="latitude").text.strip()
    longitude = soup.find("span", class_="longitude").text.strip()
    return latitude + ', ' + longitude


def capitals_locations(url):
    res = []
    links = get_capital_links(url)
    for link in links:
        lat_long = get_lat_long('https://pl.wikipedia.org' + link[2])
        res.append([link[0], link[1], lat_long])
    return res


def users_location(url):
    return get_lat_long(url)


def convert_to_decimal(coord_str):
    degrees, minutes, seconds, direction = '0', '0', '0', ''
    if '°' in coord_str:
        degrees, direction = coord_str.split('°')
        if '′' in direction:
            minutes, direction = direction.split('′')
            if '″' in direction:
                seconds, direction = direction.split('″')
    return (float(degrees.replace(',', '.')) + float(minutes.replace(',', '.')) / 60 + float(seconds.replace(',', '.')) / 3600) * (-1 if direction in ['W', 'S'] else 1)


def calculate_distance(coord1, coord2):
    # Convert coordinates to decimal format
    if type(coord1) == float or type(coord2) == float:
        return None
    coord1 = coord1.split(', ')
    coord2 = coord2.split(', ')
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    lat1, lon1 = convert_to_decimal(lat1), convert_to_decimal(lon1)
    lat2, lon2 = convert_to_decimal(lat2), convert_to_decimal(lon2)

    # Calculate distance using geodesic function
    distance = geodesic((lat1, lon1), (lat2, lon2)).km
    # print(coord1, coord2, distance)
    return distance


def write_capitals_to_csv(url):
    capitals_loc = capitals_locations(url)
    capitals_df = pd.DataFrame(capitals_loc, columns=['Country', 'Capital', 'Coordinates'])
    capitals_df.to_csv('capitals_df.csv')


if __name__ == '__main__':
    # CREATING CSV FILE WITH COUNTRY, CAPITAL and COORDINATES
    write_capitals_to_csv("https://pl.wikipedia.org/wiki/Lista_pa%C5%84stw_%C5%9Bwiata")
