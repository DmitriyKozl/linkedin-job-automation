from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
from selenium.webdriver.common.keys import Keys

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/")

"""
Signing in 
"""
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
time.sleep(2)
first_name = driver.find_element(By.XPATH, value="/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input")
first_name.send_keys(EMAIL)
time.sleep(2)

name = driver.find_element(By.NAME, value="session_password")
name.send_keys(PASSWORD)

time.sleep(2)
submit_button = driver.find_element(By.XPATH, "/html/body/main/section[1]/div/div/form/div[2]/button")
submit_button.click()
time.sleep(10)

"""
searching for jobs
"""

job_link = driver.find_element(By.XPATH, "/html/body/div[6]/header/div/nav/ul/li[3]/a")
time.sleep(2)
job_link.click()

time.sleep(5)

# job_search = driver.find_element(By.ID, "recentSearchesIndex__0")
job_search = driver.find_element(By.XPATH, "/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]")
print(job_search.text)
time.sleep(2)
job_search.click()
time.sleep(2)
job_search.send_keys("software developer")
time.sleep(2)
job_search.send_keys(Keys.ENTER)
page = 1
job_dictionary = {}
for i in range(6):
    time.sleep(2)
    jobs_list = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")
    print(len(jobs_list))
    driver.execute_script("arguments[0].scrollIntoView();", jobs_list[0])
    time.sleep(5)
    for card in jobs_list:
        try:
            time.sleep(8)
            card.click()
            print(f"Job clicked")
            time.sleep(2)
            job_name = driver.find_element(By.XPATH,
                                           "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/a/h2")
            job_skills = driver.find_element(By.XPATH,
                                             "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[6]/section[2]/div/div/div/div/a")
            company_name = driver.find_element(By.XPATH,
                                               "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/section/section/div[1]/div[1]/div/div[2]/div[1]")
            easy_applied = driver.find_element(By.XPATH,
                                               "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button")
            link_to_application_form = driver.find_element(By.XPATH,
                                                           " /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button")
            location = driver.find_element(By.XPATH,
                                           " /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/text()")
            job_type = driver.find_element(By.XPATH,
                                           "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]/span")
            # job_dictionary[job_name] = {
            #     "skills": job_skills.text,
            #     "company": company_name.text,
            #     "location": location.text,
            #     "type": job_type.text
            # }
            print(f"skills: {job_skills.text},company: {company_name.text}, type: {job_type.text}")


        except StaleElementReferenceException:
            print("Stale element reference. Skipping.")
    # driver.find_elements("xpath", f"//button[@aria-label='Page {page}']")[0].click()
    # page += 1
print(job_dictionary)
time.sleep(5)
driver.quit()

# skills:/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[6]/section[2]/div/div/div/div/a
# name : /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/a/h2
# company name /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/section/section/div[1]/div[1]/div/div[2]/div[1]
# easy applied /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button
# link to application form /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button
# location /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/text()
# type /html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]/span
