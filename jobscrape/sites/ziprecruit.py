from bs4 import BeautifulSoup


def get_jobs(html):
    """ Scrapes ziprecruiter.com"""

    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.findAll('article', class_="job_result")
    jobs_list = []

    for job in jobs:
        try:
            title = job.h2.span.text
            company = job.find('p', class_='job_org').a.text
            location = job.find('p', class_='job_org').find('a', class_='t_location_link location').text
            summary = job.find('p', class_="job_snippet").text.strip()
            link = job.a['href']
        except AttributeError:
            pass

        jobs_list.append({'title': title, 'company': company, 'location': location, 'summary': summary, "link": link})

    return jobs_list
