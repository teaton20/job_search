import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from urllib.parse import urlparse, quote_plus
from datetime import datetime, timedelta

# Update this to your job posting of choice
url = "https://jobs.intuit.com/job/mountain-view/staff-technical-data-analyst/27595/78304889536"

def get_glassdoor_link(company):
    search_query = quote_plus(f"{company} site:glassdoor.com")
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={search_query}"
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'glassdoor.com' in href:
            match = re.search(r'(https?://[\w./%-]*glassdoor\.com[^"]+)', href)
            if match:
                return match.group(1)
    return None


def extract_company_from_url(url):
    domain = urlparse(url).netloc
    company_name = domain.split('.')[-2]  # e.g., intuit.com -> 'intuit'
    return company_name.capitalize()


def scrape_job_posting(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True).lower()

    # Job title
    job_title_tag = soup.find(['h1', 'h2'])
    job_title = job_title_tag.text.strip() if job_title_tag else None

    # Company name from page or fallback to domain
    company = None
    for tag in soup.find_all(['div', 'span', 'p']):
        if 'company' in tag.get('class', []) or 'employer' in tag.get('class', []):
            company = tag.text.strip()
            break
    if not company:
        company = extract_company_from_url(url)

    # Location
    location = None
    for tag in soup.find_all(['div', 'span', 'p']):
        if 'location' in tag.get('class', []):
            location = tag.text.strip()
            break

    # Remote/Hybrid/In-Person detection
    in_person_hybrid_remote = None
    if 'remote' in text:
        in_person_hybrid_remote = 'Remote'
    elif 'hybrid' in text:
        in_person_hybrid_remote = 'Hybrid'
    elif 'on-site' in text or 'in person' in text or 'in-person' in text:
        in_person_hybrid_remote = 'In Person'

    # Salary range - look for dollar amounts in the text
    salary_matches = re.findall(r'\$\d{2,3}[,\d]*', text)
    salary_low, salary_high = None, None
    if len(salary_matches) >= 2:
        salary_low = salary_matches[0].replace('$', '').replace(',', '')
        salary_high = salary_matches[1].replace('$', '').replace(',', '')

    # Glassdoor link
    glassdoor_link = get_glassdoor_link(company) if company else None

    # Dates
    date_applied = datetime.today().strftime('%Y-%m-%d')
    follow_up_date = (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d')

    return {
        "company": company,
        "job_title": job_title,
        "location": location,
        "in_person_hybrid_remote": in_person_hybrid_remote,
        "salary_low": salary_low,
        "salary_high": salary_high,
        "link": url,
        "glassdoor": glassdoor_link,
        "resume_used": None,
        "cover_letter": None,
        "referral": None,
        "date_applied": date_applied,
        "follow_up_date": follow_up_date,
        "interview": None
    }


def write_to_csv(data, filename="job_search.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
    result = scrape_job_posting(url)
    write_to_csv(result)
    print("Job posting info added to job_search.csv!")
