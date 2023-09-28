
import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def fetch_and_parse_with_selenium(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    data = {}
    try:
        with webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options) as driver:
            driver.get(url)
            time.sleep(5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            currency_elements = soup.find_all('li', style="white-space: nowrap; float: left; padding: 0px 7px; line-height: 30px;")
            
            for elem in currency_elements:
                currency_text = elem.contents[0].strip()
                span = elem.find('span', class_='stat')
                if span:
                    stat_text = span.text.strip().replace("Buying:", "").replace("Selling:", "").split(',')
                    buying = stat_text[0].strip()
                    selling = stat_text[1].strip()
                    data[currency_text] = {'Buying': buying, 'Selling': selling}
                    
    except Exception as e:
        return jsonify({'error': str(e)})
    
    return data


@app.route('/', methods=['GET'])
def scrape():
    url_to_scrape = 'YOUR-URL-HERE' #
    scraped_data = fetch_and_parse_with_selenium(url_to_scrape)
    return jsonify(scraped_data)

if __name__ == '__main__':
    app.run()
