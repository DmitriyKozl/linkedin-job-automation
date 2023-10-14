import os

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver import Remote, ChromeOptions

load_dotenv()

SBR_WEBDRIVER = os.environ.get('SBR_WEBDRIVER')


def setup_driver():
    print('==> Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    driver = Remote(sbr_connection, options=ChromeOptions())
    print('==> Connected!')
    return driver


class Jobs:
    JOB_LINK_LOCATOR = (By.XPATH, "/html/body/nav/ul/li[4]")
    JOB_SEARCH_KEYWORD_LOCATOR = (By.NAME, "keywords")
    LOCATION_SEARCH_LOCATOR = (By.NAME, "location")
    LOCATION_EXIT_BUTTON_LOCATOR = (
    By.XPATH, "/html/body/div[1]/header/nav/section/section[2]/form/section[2]/button/icon")
    JOB_SEARCH_BAR_LOCATION_LOCATOR = (By.ID, "job-search-bar-location")
    TIME_DROPDOWN_LOCATOR = (By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[1]/div/div/button')
    PAST_MONTH_SELECTION_LOCATOR = (
    By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[1]/div/div/div/div/div/div[2]/input')
    DONE_BUTTON_LOCATOR = (By.CLASS_NAME, 'filter__submit-button')

    def __init__(self):
        self.driver = setup_driver()
        self.search_jobs()

    def click_element(self, descriptor, locator, wait_time=10):
        """Click on a web element if it exists"""
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator))
            element.click()
            print(f"==> {descriptor} clicked!")
        except NoSuchElementException:
            print(f"==> Failed to find {descriptor}")

    def send_keys_to_element(self, descriptor, locator, keys, wait_time=10):
        """Send keys to a web element if it exists"""
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator))
            element.send_keys(keys)
            print(f"==> {descriptor} received input: {keys}")
        except NoSuchElementException:
            print(f"==> Failed to find {descriptor}")

    def search_jobs(self):
        print('==> Navigating to LinkedIn...')
        self.driver.get("https://www.linkedin.com")
        time.sleep(2)

        self.click_element("Job Link", self.JOB_LINK_LOCATOR)
        self.send_keys_to_element("Job Search", self.JOB_SEARCH_KEYWORD_LOCATOR, "software developer")
        time.sleep(5)
        self.send_keys_to_element("Job Search", self.JOB_SEARCH_KEYWORD_LOCATOR, Keys.ENTER)

        self.click_element("Location Search", self.LOCATION_SEARCH_LOCATOR, 5)
        time.sleep(1)
        self.click_element("Location exit button", self.LOCATION_EXIT_BUTTON_LOCATOR, 2)
        time.sleep(1)
        self.send_keys_to_element("Location Search", self.JOB_SEARCH_BAR_LOCATION_LOCATOR,
                                  "Ghent, Flemish Region, Belgium")
        time.sleep(1)
        self.send_keys_to_element("Location Search", self.JOB_SEARCH_BAR_LOCATION_LOCATOR, Keys.ENTER)
        self.click_element("Time Dropdown", self.TIME_DROPDOWN_LOCATOR)
        self.click_element("Past Month Selection", self.PAST_MONTH_SELECTION_LOCATOR)
        self.click_element("Done Button", self.DONE_BUTTON_LOCATOR)

    def scrape_jobs(self):
        time.sleep(2)
        job_dictionary = {}
        i = 0
        while i < 7:  # Reduced to 5 pages for testing
            time.sleep(2)
            jobs_list = self.driver.find_elements(By.CSS_SELECTOR,
                                                  ".full-width.artdeco-entity-lockup__title.ember-view")
            print(len(jobs_list))
            self.driver.execute_script("arguments[0].scrollIntoView();", jobs_list[-1])
            time.sleep(5)
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".full-width.artdeco-entity-lockup__title.ember-view")))
            i += 1

            if len(jobs_list) == 25:
                for card in jobs_list:
                    try:
                        card.click()
                        print(f"Job clicked")
                        time.sleep(2)
                        job_name = card.text
                        # Locate the skills element within a try-except block to handle cases where it's not present
                        try:
                            job_skills = self.driver.find_element(By.CSS_SELECTOR,
                                                                  ".job-details-how-you-match__skills-item-subtitle")
                            job_type = self.driver.find_element(By.XPATH,
                                                                "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]/span")
                            company = self.driver.find_element(By.CSS_SELECTOR, ".app-aware-link ")
                            location = self.driver.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-item ")
                            hiring_person_profile = self.driver.find_element(By.XPATH,
                                                                             "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/a")
                            skills_text = job_skills.text
                            job_type_text = job_type.text
                            company_text = company.text
                            location_text = location.text
                            hiring_person_profile_link = hiring_person_profile.get_attribute("href")
                        except NoSuchElementException:
                            skills_text = "Skills not found"

                        print(f" name: {job_name},"
                              f" skills: {skills_text},"
                              f" job type: {job_type_text},"
                              f" company: {company_text},"
                              f" location:{location_text}, "
                              f" recruiter: {hiring_person_profile_link}")

                    except StaleElementReferenceException:
                        print(
                            "Stale element reference. Skipping.")
                        # self.driver.find_elements("xpath", f"//button[@aria-label='Page {page}']")[0].click()
                        # page += 1
        print('==> Stopping driver...')
        self.driver.quit()
        print('==> Driver stopped!')


    def run(self):
        time.sleep(2)
        self.scrape_jobs()
        self.driver.quit()
