from bs4 import BeautifulSoup


def get_jobs(html):
    """Scrapes indeed.com"""

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('table', id="pageContent")
    jobs = results.findAll('div', class_="row", attrs={'data-tn-component': 'organicJob'})
    jobs_list = []

    for job in jobs:

        # Each posting can have some missing fields, which leads to attribute errors when parsing that field
        # Catch on a case-by-case basis so we don't discard the entire posting
        try:
            title = job.h2.a.text
        except AttributeError:
            title = 'Unknown'
        try:
            company = job.find('span', class_='company').text.strip()
        except AttributeError:
            company = 'Unknown'
        try:
            location = job.find('span', class_='location').text
        except AttributeError:
            location = 'Unknown'
        try:
            summary = job.table.find('span', class_='summary').text.strip()
        except AttributeError:
            summary = 'Unknown'
        try:
            link = "https://www.indeed.com" + job.h2.a.get("href")
        except AttributeError:
            link = 'Unknown'

        jobs_list.append({'title': title, 'company': company, 'location': location, 'summary': summary, "link": link})

    return jobs_list
