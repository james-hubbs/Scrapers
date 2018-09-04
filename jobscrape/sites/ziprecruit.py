from bs4 import BeautifulSoup


def get_jobs(html):
    """Scrapes ziprecruiter.com"""

    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.findAll('article', class_="job_result")
    jobs_list = []

    for job in jobs:

        # Each posting can have some missing fields, which leads to attribute errors when parsing that field
        # Catch on a case-by-case basis so we don't discard the entire posting
        try:
            title = job.h2.span.text
        except AttributeError:
            title = 'Unknown'
        try:
            company = job.find('p', class_='job_org').a.text
        except AttributeError:
            company = 'Unknown'
        try:
            location = job.find('p', class_='job_org').find('a', class_='t_location_link location').text
        except AttributeError:
            location = 'Unknown'
        try:
            summary = job.find('p', class_="job_snippet").text.strip()
        except AttributeError:
            summary = 'Unknown'
        try:
            link = job.a['href']
        except AttributeError:
            link = 'Unknown'

        jobs_list.append({'title': title, 'company': company, 'location': location, 'summary': summary, "link": link})

    return jobs_list
