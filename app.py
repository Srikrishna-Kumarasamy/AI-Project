import pandas as pd
from zenml.steps import step
from store_in_qdrant import Qdrant
from zenml.pipelines import pipeline
from store_in_mongo_db import MongoDB
from scrappers.youtube_scrapper import YoutubeScrapper
from scrappers.generic_scrapper import GenericScrapper

mongo_db = MongoDB()

@step
def extract_ros2_documentations() -> list:
    generic_scrapper = GenericScrapper()
    ros2_documentations_df = pd.read_csv("generic_webpages.csv")
    seen_urls = set()
    documents = []
    for index, row in ros2_documentations_df.iterrows():
        try:
            sub_documents, seen_urls = generic_scrapper.scrape(seen_urls, row['title'], row['url'])
            documents.extend(sub_documents)
        except Exception as e:
            print("Error :", row['url'], e)
    return documents

@step
def extract_ros2_youtube_videos() -> list:
    youtube_scrapper = YoutubeScrapper()
    youtube_df = pd.read_csv("youtube_urls.csv")
    documents = []
    for index, row in youtube_df.iterrows():
        try:
            document = youtube_scrapper.scrape(row["url"])
            documents.append(document)
        except Exception as e:
            print("Error")
    return documents

@step
def store_in_mongo(documents : list) -> None:
    for document in documents:
        mongo_db.insert(document)

@step
def chunk_and_store_in_qdrant():
    mongo_db = MongoDB()
    qdrant_db = Qdrant()
    documents = mongo_db.get_all_docs()
    for index, document in enumerate(documents):
        qdrant_db.store_in_qdrant(document)
        print(f"{index} Embeddings stored")

@pipeline
def pipeline():
    ros2_documents = extract_ros2_documentations()
    store_in_mongo(documents=ros2_documents, after="extract_ros2_documentations")
    youtube_documents = extract_ros2_youtube_videos()
    store_in_mongo(documents=youtube_documents, after="extract_ros2_youtube_videos")
    chunk_and_store_in_qdrant(after=["store_in_mongo", "store_in_mongo_2"])

if __name__ == "__main__":
    pipeline.with_options(enable_cache=False)()

# chunk_and_store_in_qdrant()
