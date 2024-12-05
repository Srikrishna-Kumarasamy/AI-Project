import uuid
import ollama
import tiktoken
from semchunk import chunk
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.http.models import VectorParams
from qdrant_client.models import VectorParams, Distance, PointStruct

class Qdrant:

    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        if not self.client.collection_exists("rag_data"):    
            self.client.create_collection(
                collection_name="rag_data",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def get_embeddings(self, document):
        embedding_response = ollama.embeddings(
            model='all-minilm:33m', 
            prompt=document
        )
        return embedding_response['embedding']
    
    def get_chunks(self, document_data):
        def num_tokens(text: str) -> int:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            return len(encoding.encode(text))

        chunker = chunk
        chunk_size = 300
        chunks = chunker(document_data, chunk_size, num_tokens)
        return chunks

    def store_in_qdrant(self, document):
        document_data = f"Title : {document['title']}\nContent : {document['description']}"
        chunks = self.get_chunks(document_data)
        for chunk in chunks:
            embeddings = self.get_embeddings(chunk)
            payload = {
                "_id" : document["_id"],
                "title" : document["title"],
                "source" : document["source"],
                "url" : document["url"],
                "description" : chunk,
                "additional_info" : document["additional_info"]
            }
            self.client.upsert(
                collection_name="rag_data",
                points=[
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embeddings,
                        payload=payload
                    )
                ]
            )
        return True
