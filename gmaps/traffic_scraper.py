""" traffic_scraper.py: A simple script to scrape travel time data from Google's Distance Matrix API."""


import os
import urllib.request
import time
import datetime
import csv
import sys
import json
import argparse


def scrape(begin, end, key, period, duration, file_name):
    """
    Scrapes travel duration data from Google's Distance Matrix API

    Parameters:
        begin: start location (GPS coordinates)
        end: end location (GPS coordinates)
        key: Google Distance Matrix API key
        period: Time in minutes between scrapes
        duration: Total time in minutes to scrape for

    Returns:
        Nothing. Writes scraped data to CSV.

    """

    # Construct the request URL
    base = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    locations = 'origins={}&destinations={}&departure_time=now&'.format(begin, end)
    extras = 'units=imperial&'
    api_key = 'key=' + key

    url = base + locations + extras + api_key

    # Request data and convert from json to dictionary
    data = json.loads(request_data(url))
    # Close program if API key or location were invalid
    check_data(data)

    # Write data into the data directory
    os.chdir('.\data')

    print("Scraping...")
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        # Headers
        writer.writerow(["Timestamp", "Travel Time (mins)", "Time Due to Traffic (mins)"])

        num_points = 0  # Number of data points scraped so far
        while num_points <= int(duration / period):

            # Request data and convert from json to dictionary
            data = json.loads(request_data(url))

            # Get travel time from data
            travel_time = round(data['rows'][0]['elements'][0]['duration_in_traffic']['value'] / 60, 2)

            # Calculate time due to traffic
            average_time = round(data['rows'][0]['elements'][0]['duration']['value'] / 60, 2)
            due_to_traffic = round(travel_time - average_time, 2)

            # Write data to a new row
            writer.writerow((datetime.datetime.now(), travel_time, due_to_traffic))

            num_points += 1
            if num_points % 5 == 0:
                print("{} data points have been scraped... ".format(num_points))
            # Wait until next period
            time.sleep(period * 60)


def request_data(link):
    """
    Attempts to read HTML data from provided link.
    Will retry 3 times if error occurs.

    """
    success = False
    num_retries = 0

    while success is False:
        try:
            # Request and open URL
            request = urllib.request.Request(link)
            response = urllib.request.urlopen(request)

            # 200 is success code
            if response.getcode() == 200:
                success = True

        except (ValueError, urllib.request.URLError):
            print("Unable to contact {}".format(link))

            if num_retries < 2:
                print("Retrying in 5 seconds...")
                num_retries += 1
                time.sleep(5)
            else:
                print("Failed to connect after 3 attempts.")
                sys.exit()

    return response.read()


def check_data(data):
    """Closes program if API key or location were invalid"""

    # Check to ensure access was granted
    if data['status'] == 'REQUEST_DENIED':
        print("Invalid API key")
        sys.exit()

    # Check to ensure location is valid
    if data['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
        print("Invalid location")
        sys.exit()


if __name__ == '__main__':
    key = os.environ.get("GMAPSKEY")  # Key should be stored in an environmental variable
    if key is None:
        key = input("Enter API key: ")

    # Allow file name to be inputted as command-line parameter
    parser = argparse.ArgumentParser(description="Scrape traffic data from Google Maps.")
    parser.add_argument('-f', '--file_name', type=str, metavar='', required=False, default="traffic_data.csv",
                        help="Name of CSV file to create. Default is traffic_data.csv")
    args = parser.parse_args()

    origin = input("Enter starting point:").replace(" ", "").strip()  # '40.858494,-73.212364'
    destination = input("Enter destination:").replace(" ", "").strip()  # '40.856183,-73.186404'
    period = float(input("Enter period in minutes (how often to scrape data):"))
    duration = float(input("Enter total duration in minutes:"))

    scrape(origin, destination, key, period, duration, args.file_name)
