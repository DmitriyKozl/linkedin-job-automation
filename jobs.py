from selenium import webdriver
from seleniumwire import webdriver
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver import Remote, ChromeOptions

load_dotenv()


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


class Jobs:
    def __init__(self):
        self.driver = setup_driver()
        self.login()
        self.search_jobs()

    def login(self):
        time.sleep(2)
        EMAIL = os.environ.get('EMAIL')
        PASSWORD = os.environ.get('PASSWORD')
        self.driver.get("https://www.linkedin.com/")

        time.sleep(2)

        first_name = self.driver.find_element(By.XPATH,
                                              value="/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input")
        first_name.send_keys(EMAIL)

        time.sleep(2)

        name = self.driver.find_element(By.NAME, value="session_password")
        name.send_keys(PASSWORD)

        time.sleep(2)

        submit_button = self.driver.find_element(By.XPATH, "/html/body/main/section[1]/div/div/form/div[2]/button")
        submit_button.click()

        time.sleep(10)

    def search_jobs(self):
        time.sleep(2)

        job_link = self.driver.find_element(By.XPATH, "/html/body/div[6]/header/div/nav/ul/li[3]/a")
        time.sleep(2)

        job_link.click()
        time.sleep(5)

        job_search = self.driver.find_element(By.XPATH,
                                              "/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]")

        time.sleep(2)
        job_search.click()

        time.sleep(2)
        job_search.send_keys("software developer")

        time.sleep(2)
        job_search.send_keys(Keys.ENTER)

    def scrape_jobs(self):
        time.sleep(2)
        page = 1
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
                        print("Stale element reference. Skipping.")
                # self.driver.find_elements("xpath", f"//button[@aria-label='Page {page}']")[0].click()
                # page += 1

    def run(self):
        time.sleep(2)
        self.scrape_jobs()
        self.driver.quit()
