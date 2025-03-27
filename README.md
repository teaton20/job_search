# job_search
A custom job search tool that, given a link to a job posting, auto-populates a spreadsheet for easy reference to all of its information.

## Features

- Scrapes job listings for:
  - Job title
  - Company
  - Location
  - Salary range
  - Work mode (Remote / Hybrid / In Person)
  - Glassdoor link
- Appends structured data to a CSV (`job_search.csv`)
- Auto-syncs CSV to Google Drive
- Uses Google Sheets Apps Script to:
  - Auto-import new rows at any desired frequency
  - Prevent overwriting manual edits
  - Update only when data changes

## Tech Stack

- Python (Requests, BeautifulSoup)
- Google Apps Script
- CSV / Google Drive Sync
- Google Sheets Integration

## How to Use

1. Clone this repo.
2. Run `job_scraper.py` with a job listing URL of your choice.
3. Ensure `job_search.csv` is syncing to Google Drive.
4. Link your Google Sheet to the CSV using the provided Apps Script.
5. You're ready to go! The Google Sheet should auto-populate every 5 minutes if there is new content added to the CSV.

## In This Repo

- `job_search.csv`: The blank CSV canvas for the spreadsheet to keep track of jobs with.
- `job_search.py`: The Python file for executing the tool.
- `job_search.ipynb`: The same Python code, but in a Jupyter notebook if that is preferred.

## To-Do / Wishlist

- [ ] Add CLI support for multiple URLs
- [ ] Auto-email alerts for new interviews
- [ ] Resume/cover letter matcher integration
