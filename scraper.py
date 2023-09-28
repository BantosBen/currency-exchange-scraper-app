
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def fetch_and_parse_with_selenium(url):
    # Create a new instance of the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    service = Service('D:\setup\chromedriver-win64\chromedriver.exe')
    
    try:
        with webdriver.Chrome(service=service, options=chrome_options) as driver:
            # Navigate to the URL
            driver.get(url)
            
            # Allow time for JavaScript to load
            time.sleep(5)          
            
            # Parse the Selenium WebDriver page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find the relevant <li> elements (adjust the search criteria as needed)
            currency_elements = soup.find_all('li', style="white-space: nowrap; float: left; padding: 0px 7px; line-height: 30px;")

            for elem in currency_elements:
                # Extract currency
                currency_text = elem.contents[0].strip()
                
                # Extract buying and selling rates
                span = elem.find('span', class_='stat')
                if span:
                    stat_text = span.text.strip().replace("Buying:", "").replace("Selling:", "").split(',')
                    buying = stat_text[0].strip()
                    selling = stat_text[1].strip()
                
                print(f"Currency: {currency_text}, Buying: {buying}, Selling: {selling}")

            
            # Add a delay to respect the website's rate limits (adjust time as needed)
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_url_here' with the actual URL you want to scrape
url_to_scrape = 'https://equitygroupholdings.com/ke/index.php'
fetch_and_parse_with_selenium(url_to_scrape)
