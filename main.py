from jobs import Jobs
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    jobs_scraper = Jobs()
    jobs_scraper.run()

