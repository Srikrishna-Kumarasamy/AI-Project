import pandas as pd
from store_in_qdant import Qdrant
from store_in_mongo_db import MongoDB
from scrappers.youtube_scrapper import YoutubeScrapper

qdrant_db = Qdrant()
youtube_scrapper = YoutubeScrapper()

# Reading Sample documents from user
documents_df = pd.read_csv("sample_data.csv")

for row, document in documents_df.iterrows():
    try:
        document = youtube_scrapper.scrape_and_store(document["url"])
    except Exception as e:
        print("Error")
print("Scrapping Done")


mongo_db = MongoDB()
documents = mongo_db.get_all_docs()

for document in documents:
    qdrant_db.store_in_qdrant(document)
print("Uploaded to qdrant done")
print(documents)