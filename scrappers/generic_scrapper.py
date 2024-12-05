import os
import uuid
import requests
from bs4 import BeautifulSoup
from dataclasses import asdict
from store_in_mongo_db import MongoDB
from data_modules.content import Content

class GenericScrapper:

    def __init__(self):
        self.SOURCE = "ROS Documentations"
        self.mongo_db = MongoDB()

    def store(self, content, title, url):
        content = Content(
            _id = str(uuid.uuid4()),
            title = title,
            source = self.SOURCE,
            url = url,
            description = content
        )
        self.mongo_db.insert(asdict(content))

    def scrape_page_with_headings(self, url):
        print(f"Scraping URL: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("http") or href.startswith("/"):
                # Normalize relative links to absolute
                full_url = href if href.startswith("http") else os.path.join(os.path.dirname(url), href)
                links.append({"text": a_tag.get_text(strip=True), "url": full_url})

        content_by_headings = {}
        current_heading = "General"
        for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            if element.name in ["h1", "h2", "h3", "h4"]:
                current_heading = element.get_text(strip=True)
                content_by_headings[current_heading] = []
            else:
                text = element.get_text(strip=True)
                if current_heading not in content_by_headings:
                    content_by_headings[current_heading] = []
                content_by_headings[current_heading].append(text)

        for heading in content_by_headings:
            content_by_headings[heading] = " ".join(content_by_headings[heading])

        page_content = ""
        for heading, paragraph in content_by_headings.items():
            page_content += f"\n{heading}\n{paragraph}\n"
        return page_content, links

    def scrape(self, title, base_url):
        # Scrape Main page
        main_page_content, links = self.scrape_page_with_headings(base_url)
        self.store(main_page_content, title, base_url)

        # Scrape Secondary pages
        for link in links:
            page_content, secondary_links = self.scrape_page_with_headings(link['url'])
            self.store(page_content, link['text'], link['url'])
