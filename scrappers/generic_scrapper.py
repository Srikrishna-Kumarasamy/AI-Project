import os
import uuid
import requests
import validators
from bs4 import BeautifulSoup
from selenium import webdriver
from dataclasses import asdict
from store_in_mongo_db import MongoDB
from data_modules.content import Content

class GenericScrapper:

    def __init__(self):
        self.SOURCE = "ROS Documentations"
        self.mongo_db = MongoDB()

    def transform(self, content, title, url):
        content = Content(
            _id = str(uuid.uuid4()),
            title = title,
            source = self.SOURCE,
            url = url,
            description = content
        )
        return asdict(content)

    def get_response_from_selenium(self, url):
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(10)
        driver.get(url)
        page_content = driver.page_source
        driver.quit()
        return page_content

    def scrape_page_with_headings(self, url):
        print(f"Scraping URL: {url}")
        response = requests.get(url, timeout=10)
        response = response.text
        soup = BeautifulSoup(response, 'lxml')
        page_content = soup.get_text(separator="\n", strip=True)
        links = []
        for link in soup.find_all('a', href=True): 
            href = link['href']
            if href.startswith("http") or href.startswith("/"):
                full_url = href if href.startswith("http") else os.path.join(os.path.dirname(url), href)
                if validators.url(full_url):
                    links.append({"text": link.get_text(strip=True), "url": full_url})
        return page_content, links

    def scrape(self, seen_urls, title, base_url):
        # Scrape Main page
        documents = []
        main_page_content, links = self.scrape_page_with_headings(base_url)
        documents.append(self.transform(main_page_content, title, base_url))
        # Scrape Secondary pages
        for link in links:
            try:
                if link['url'] in seen_urls:
                    continue
                seen_urls.add(link['url'])
                page_content, secondary_links = self.scrape_page_with_headings(link['url'])
                documents.append(self.transform(page_content, link['text'], link['url']))
            except Exception as e:
                print("Scrape Error")
        return documents, seen_urls
