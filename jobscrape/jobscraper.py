"""
jobscrape.py: A web-scraping tool to speed up your job/internship search

"""
import os.path
import sys
import urllib.request
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from jobscrape.initialize import check
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


def scrape():
    """Scrapes job postings"""
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

    # Check that data directory and userdata.json exist
    check()

    print("Scraping...\n")
    postings = scrape()

    print("{} postings scraped\n".format(len(postings)))

    print_jobs(postings)
