"""
jobscrape.py: A web-scraping tool to speed up your job/internship search

"""
import os.path
import sys
import urllib.request
import time
import json
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from jobscrape.initialize import check, update_user_data
from jobscrape.sites import indeed, ziprecruit


def request_html(link):
    """
    Attempts to read HTML data from provided link.
    Will retry 3 times if error occurs.

    """
    success = False
    num_retries = 0

    while success is False:
        try:
            # Request and open URL
            request = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(request)

            # 200 is success code
            if response.getcode() == 200:
                success = True

        except (ValueError, urllib.request.URLError) as e:
            print("Unable to contact {}".format(link))
            print(e)

            if num_retries < 2:
                print("Retrying in 5 seconds...")
                num_retries += 1
                time.sleep(5)
            else:
                print("Failed to connect after 3 attempts.")
                sys.exit()

    return response.read()


def print_jobs(jobs):
    """Prints a list of jobs"""
    for job in jobs:
        print('Title: {}\nCompany: {}\nLocation: {}\nSummary: {}\nLink: {}\n'.format(job['title'], job['company'], job['location'], job['summary'], job['link']))


def write_csv(jobs):
    """Writes a list of jobs to csv file"""

    with open("data/jobs.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        # Headers
        writer.writerow(['Title', 'Company', 'Location', 'Summary', 'Link'])

        # Write each job to a new row
        for job in jobs:
            writer.writerow([job['title'], job['company'], job['location'], job['summary'], job['link']])

        print("\nCreated jobs.csv in {}\data".format(os.getcwd()))


def scrape():
    """Scrapes recent job postings from indeed.com and ziprecruiter.com"""

    # Read data from userdata.json
    with open('data/userdata.json', 'r') as file:
        user_data = json.load(file)

    # URLs
    zip_url = 'https://www.ziprecruiter.com/candidate/search?search={}&location={}&days=5&radius={}' \
              '&refine_by_tags=employment_type%3Ainternship'.format(user_data['keywords'],
                                                                    user_data['location'],
                                                                    user_data['radius'])

    indeed_url = 'https://www.indeed.com/jobs?q={}&l={}&sort=date&radius={}'.format(user_data['keywords'],
                                                                                    user_data['location'],
                                                                                    user_data['radius'])

    zip_html = request_html(zip_url)
    indeed_html = request_html(indeed_url)

    zip_jobs = ziprecruit.get_jobs(zip_html)
    indeed_jobs = indeed.get_jobs(indeed_html)

    return zip_jobs + indeed_jobs

if __name__ == '__main__':

    # Check if data/userdata.json exists
    exists = check()

    if exists:
        # Read data from userdata.json
        with open('data/userdata.json', 'r') as file:
            user_data = json.load(file)

            # Ask to update
            print("Current query values are keywords={}, location={}, radius={}".format(user_data['keywords'], user_data['location'], user_data['radius']))
            update = input("Update search query values? (Y/N):").strip().lower()
            if update == 'y':
                update_user_data()

    else:
        update_user_data()

    print("Scraping...\n")
    postings = scrape()

    print("{} job postings scraped".format(len(postings)))

    view = input("Print postings? (Y/N):").strip().lower()[0]
    if view == 'y':
        print_jobs(postings)

    write = input("Write to CSV? (Y/N):").strip().lower()[0]
    if write == 'y':
        write_csv(postings)
