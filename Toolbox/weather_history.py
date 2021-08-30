import sys
import datetime
import csv
import urllib.parse
import requests
from get_weather import search_city

from get_weather import BASE_URI



def daily_forecast(woeid, year, month, day):
    url = urllib.parse.urljoin(BASE_URI,
                               f"/api/location/{woeid}/{year}/{month}/{day}")
    return requests.get(url).json()

def monthly_forecast(woeid, year, month):
    """ return a `list` of forecasts for the whole month """
    forecasts = []
    date = datetime.date(year, month, 1)
    if month == 12:
        upper_bound = datetime.date(year + 1, 1, 1)
    else:
        upper_bound = datetime.date(year, month + 1, 1)
    while date < upper_bound:
        print(f"Fetching forecast for {date.strftime('%Y-%m-%d')}")
        forecasts += daily_forecast(woeid, date.year, date.month, date.day)
        date = date + datetime.timedelta(days=1)
    return forecasts


def write_csv(woeid, year, month, city, forecasts):
    """ dump all the forecasts to a CSV file in the `data` folder """
    filename = f"{year}_{'{:02d}'.format(month)}_{woeid}_{city.lower()}"
    with open(f"data/{filename}.csv", 'w') as output_file:
        keys = forecasts[0].keys()
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(forecasts)


def main():
    if len(sys.argv) > 2:
        city = search_city(sys.argv[1])
        if city:
            woeid = city['woeid']
            year = int(sys.argv[2])
            month = int(sys.argv[3])
            if 1 <= month <= 12:
                forecasts = monthly_forecast(woeid, year, month)
                if not forecasts:
                    print("Sorry, could not fetch any forecast")
                else:
                    write_csv(woeid, year, month, city['title'], forecasts)
            else:
                print("MONTH must be a number between 1 (Jan) and 12 (Dec)")
                sys.exit(1)
    else:
        print("Usage: python history.py CITY YEAR MONTH")
        sys.exit(1)


if __name__ == '__main__':
    main()
