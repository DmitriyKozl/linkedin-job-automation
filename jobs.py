import os
import traceback

import pandas
import requests
import csv
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, UnknownMethodException, \
    TimeoutException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from job_information_extractor import JobInformationExtractor
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver import Remote, ChromeOptions
from urllib.parse import urlparse, parse_qs

from job import Job

load_dotenv()


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
    chrome_options.add_argument('start-maximized')  # Start maximized
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


class Jobs:
    def __init__(self):
        self.driver = setup_driver()
        self.login()
        self.search_jobs()
        self.job_info_extractor = JobInformationExtractor(self.driver)

    def login(self):
        wait = WebDriverWait(self.driver, 10)

        print("Logging in...")
        self.driver.get("https://www.linkedin.com/login")

        # Use environment variables to fetch credentials
        username = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')

        print("Locate email field and send the email")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        print("Locate password field and send the password")
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        print("Locate and click the submit button")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()

    def search_jobs(self):
        wait = WebDriverWait(self.driver, 10)
        print("Searching for jobs...")
        # Navigate to the "Jobs" section
        jobs_link = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.app-aware-link.global-nav__primary-link[href='https://www.linkedin.com/jobs/?']")))
        jobs_link.click()

        # Find the job search bar and enter a job title
        job_search = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))
        time.sleep(2)
        job_search.send_keys("software developer")
        time.sleep(2)
        job_search.send_keys(Keys.ENTER)

    def scroll_job_list(self):
        time.sleep(2)
        job_list_count = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list__subtitle")
        print(job_list_count.text)
        jobs_list = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
        time.sleep(2)
        print(f"Currently Loaded Jobs: {len(jobs_list)}")
        self.driver.execute_script("arguments[0].scrollIntoView();", jobs_list[1])
        time.sleep(5)
        if jobs_list:
            self.driver.execute_script("arguments[0].scrollIntoView();", jobs_list[-1])
            time.sleep(5)
        return jobs_list

    def scrape_jobs(self):
        page = 1
        max_pages = 7

        for _ in range(max_pages):
            try:
                jobs_list = self.scroll_job_list()

                for job_card in jobs_list:
                    time.sleep(5)
                    self.extract_job_information(job_card)  # Find the current page's button
                current_page_li = self.driver.find_element(By.CSS_SELECTOR,
                                                           "li.artdeco-pagination__indicator--number.active.selected")
                # Find the next page's button
                next_page_li = current_page_li.find_element(By.XPATH, "following-sibling::li")
                next_page_button = next_page_li.find_element(By.TAG_NAME, "button")

                if next_page_button:
                    next_page_button.click()
                    print(f"Navigated to page {page + 1}")
                    time.sleep(2)  # Wait for the next page to load
                else:
                    print("No next page button found. Exiting.")
                    break  # No next page button found, exit the loop
            except (NoSuchElementException, TimeoutException) as e:
                print("Error occurred while extracting job information or scrolling down")
                print(traceback.format_exc())  # This will print the full traceback
                print(e)  # This will print the exception message
                break  # If an error occurs, break out of the loop

            page += 1

    def extract_job_information(self, job_card):
        try:
            job_card.click()
            print(f"Job clicked")
            job_type_text = self.job_info_extractor.get_job_type_text()
            skills = self.job_info_extractor.extract_skills()
            recruiter_link = self.job_info_extractor.get_recruiter_link()
            company = self.job_info_extractor.get_company()
            job_position = company.get("job_position")
            company_name = company.get("company_name")
            company_location = company.get("company_location")

            print(f"Job Type: {job_type_text}")
            print(f"Skills: {', '.join(skills)}")  # This will print the list as a comma-separated string
            print(f"Recruiter Link: {recruiter_link}")
            print(f"Job Position: {job_position}")
            print(f"Company Name: {company_name}")
            print(f"Company Location: {company_location}")

        except StaleElementReferenceException:
            print("Stale element reference. Skipping.")

    def run(self):
        time.sleep(2)
        self.scrape_jobs()
        self.driver.quit()
