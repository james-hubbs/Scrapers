import re
import urllib.request
from bs4 import BeautifulSoup


def get_jobs(html):
    """Scrapes Monster.com"""

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('div', class_="mux-search-results")
    jobs = results.findAll('section', class_="card-content")
    jobs_list = []

    for job in jobs:

        # Each posting can have some missing fields, which leads to attribute errors when parsing that field
        # Catch on a case-by-case basis so we don't discard the entire posting
        try:
            title = job.find('h2', class_="title").text.strip()
        except AttributeError:
            title = 'Unknown'
        try:
            company = job.find('div', class_="company").text.strip()
        except AttributeError:
            company = 'Unknown'
        try:
            location = job.find('div', class_="summary").find('div', class_="location").text.strip()
        except AttributeError:
            location = 'Unknown'
        try:
            link = job.find('h2', class_="title").a['href']
        except AttributeError:
            link = 'Unknown'

        # Monster stores job summaries on a separate page
        # Attempt to open that page and parse
        if link != 'Unknown':

            try:
                # Request and open URL
                request = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(request)

                description_page = BeautifulSoup(response.read(), 'html.parser')

                # Parse the summary text (nested in multiple divisions)
                summary = description_page.find('div', class_="row").find('div', class_="col-md-9").find('div', id="JobBody").find('div', class_="details-content").text
                # Replace redundant spaces
                summary = re.sub('\s+', ' ', summary).strip()

            except (ValueError, urllib.request.URLError, AttributeError) as e:
                summary = 'None'

        jobs_list.append({'title': title, 'company': company, 'location': location, 'summary': summary, "link": link})

    return jobs_list
