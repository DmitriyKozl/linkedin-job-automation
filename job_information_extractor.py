from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, UnknownMethodException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class JobInformationExtractor:
    def __init__(self, driver):
        self.driver = driver

    def get_job_type_text(self):
        try:
            job_type = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-insight"))
            )
            return job_type.text
        except (NoSuchElementException, TimeoutException):
            print("Job type not found.")
            return None

    def get_job_name(self):
        try:
            job_name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.job-details-jobs-unified-top-card__job-title"))
            )
            return job_name.text
        except (NoSuchElementException, TimeoutException):
            print("Job name not found.")
            return None

    def get_recruiter_link(self):
        try:
            recruiter = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".hirer-card__hirer-information.app-aware-link "))
            )
            recruiter_link = recruiter.get_attribute("href")
            return recruiter_link
        except (NoSuchElementException, TimeoutException):
            print("reqruiter link  not found.")
            return None

    def extract_skills(self):
        skills = []
        try:
            job_skills_i_match = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.app-aware-link.job-details-how-you-match__skills-item-subtitle.t-14.overflow-hidden'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", job_skills_i_match)
            skills_text = f"{job_skills_i_match.text}"
            skills = re.split(r" , | , and ", skills_text)

        except (NoSuchElementException, TimeoutException):
            print("Skills not found.")

        return skills

    def get_company(self):

        company_name =  WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".job-card-list__entity-lockup < .artdeco-entity-lockup__content < .artdeco-entity-lockup__subtitle.ember-view"))
            )
        job_position = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.job-details-jobs-unified-top-card__job-title"))
        )
        company_location = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-entity-lockup__caption ember-view < ul.job-card-container__metadata-wrapper < li.job-card-container__metadata-item"))
        )
        company = {
            "company_name": company_name.text,
            "job_position": job_position.text,
            "company_location": company_location.text
        }

        return company
