# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time
import logging
from datetime import datetime
from app.utils import clean_text, format_salary, setup_selenium_driver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _make_request(self, url, method='get', data=None, retry_count=3):
        for attempt in range(retry_count):
            try:
                if method.lower() == 'get':
                    response = self.session.get(url, headers=self.headers, timeout=10)
                else:
                    response = self.session.post(url, headers=self.headers, json=data, timeout=10)
                response.raise_for_status()
                return response
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for URL {url}: {str(e)}")
                if attempt == retry_count - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.driver = setup_selenium_driver()
        
    def scrape(self):
        jobs = []
        search_url = "https://www.linkedin.com/jobs/search/?keywords=desenvolvedor%20junior&location=Brasil"
        
        try:
            self.driver.get(search_url)
            self._scroll_to_load_all_jobs()
            
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
            
            for card in job_cards:
                try:
                    job_data = self._extract_job_data(card)
                    if job_data and self._is_junior_position(job_data['title']):
                        jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error extracting job data: {str(e)}")
                    continue
                    
        finally:
            self.driver.quit()
            
        return jobs
    
    def _scroll_to_load_all_jobs(self):
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    def _extract_job_data(self, card):
        title = card.find_element(By.CLASS_NAME, "job-card-list__title").text
        company = card.find_element(By.CLASS_NAME, "job-card-container__company-name").text
        location = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
        link = card.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
        
        return {
            'title': clean_text(title),
            'company': clean_text(company),
            'location': clean_text(location),
            'link': link,
            'platform': 'LinkedIn',
            'posted_date': datetime.utcnow()
        }

class GlassdoorScraper(BaseScraper):
    def scrape(self):
        jobs = []
        base_url = "https://www.glassdoor.com.br/Vaga/brasil-desenvolvedor-junior-vagas-SRCH_IL.0,6_IN241_KO7,26.htm"
        
        try:
            response = self._make_request(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_listings = soup.find_all('div', class_='react-job-listing')
            
            for job in job_listings:
                try:
                    job_data = self._extract_job_data(job)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error extracting Glassdoor job: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Glassdoor: {str(e)}")
            
        return jobs
    
    def _extract_job_data(self, job_element):
        title = job_element.find('a', class_='jobLink').text.strip()
        company = job_element.find('div', class_='empNameCell').text.strip()
        location = job_element.find('span', class_='loc').text.strip()
        link = 'https://www.glassdoor.com.br' + job_element.find('a', class_='jobLink')['href']
        
        return {
            'title': clean_text(title),
            'company': clean_text(company),
            'location': clean_text(location),
            'link': link,
            'platform': 'Glassdoor',
            'posted_date': datetime.utcnow()
        }

class GupyScraper(BaseScraper):
    def scrape(self):
        jobs = []
        search_url = "https://portal.api.gupy.io/api/job?name=desenvolvedor%20junior"
        
        try:
            response = self._make_request(search_url)
            jobs_data = response.json()
            
            for job in jobs_data['data']:
                try:
                    job_data = self._extract_job_data(job)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error extracting Gupy job: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Gupy: {str(e)}")
            
        return jobs
    
    def _extract_job_data(self, job_json):
        return {
            'title': clean_text(job_json['name']),
            'company': clean_text(job_json['company']['name']),
            'location': clean_text(job_json['location']),
            'link': f"https://vaga.gupy.io/{job_json['slug']}",
            'platform': 'Gupy',
            'posted_date': datetime.fromisoformat(job_json['publishedDate'])
        }
