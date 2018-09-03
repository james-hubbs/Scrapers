from bs4 import BeautifulSoup


def get_jobs(html):
    """Scrapes indeed.com"""

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('table', id="pageContent")
    jobs = results.findAll('div', class_="row", attrs={'data-tn-component': 'organicJob'})
    jobs_list = []

    for job in jobs:
        try:
            title = job.h2.a.text
            # company = job.find('div', style='display: block').span.text.strip()
            company = job.find('span', class_='company').text.strip()
            location = job.find('span', class_='location').text
            summary = job.table.find('span', class_='summary').text.strip()
            link = "https://www.indeed.com" + job.h2.a.get("href")
        except AttributeError:
            pass

        jobs_list.append({'title': title, 'company': company, 'location': location, 'summary': summary, "link": link})

    return jobs_list
