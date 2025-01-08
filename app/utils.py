# utils.py
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

logger = logging.getLogger(__name__)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def format_salary(salary_text):
    if not salary_text:
        return None
        
    salary_text = clean_text(salary_text.lower())
    
    # Remove currency symbols and dots
    salary_text = re.sub(r'[r$\.]', '', salary_text)
    
    # Try to extract salary range
    matches = re.findall(r'(\d+[,\d]*)', salary_text)
    if len(matches) >= 2:
        min_salary = float(matches[0].replace(',', '.'))
        max_salary = float(matches[1].replace(',', '.'))
        return f"R$ {min_salary:.2f} - R$ {max_salary:.2f}"
    elif len(matches) == 1:
        salary = float(matches[0].replace(',', '.'))
        return f"R$ {salary:.2f}"
        
    return None

def setup_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        logger.error(f"Error setting up Selenium driver: {str(e)}")
        raise

def is_junior_position(title):
    junior_keywords = ['junior', 'jr', 'júnior', 'trainee', 'entrada']
    title_lower = title.lower()
    
    return any(keyword in title_lower for keyword in junior_keywords)