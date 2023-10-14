from jobs import Jobs
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    print("###################################")
    print("#   LinkedIn Job Search Automation   #")
    print("###################################\n")
    jobs_scraper = Jobs()
    jobs_scraper.run()

