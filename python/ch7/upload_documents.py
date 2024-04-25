import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt  
import pandas as pd
import os  

@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
async def generate_embeddings(kernel: sk.Kernel, text):
    e = await kernel.get_service("emb").generate_embeddings(text)
    return e[0]

async def main():
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    embedding_gen = sk_oai.OpenAITextEmbedding(service_id="emb", ai_model_id="text-embedding-3-small", api_key=api_key)
    kernel.add_service(embedding_gen)
    
    index_name = os.getenv("ARXIV_SEARCH_INDEX_NAME")
    service_name = os.getenv("ARXIV_SEARCH_SERVICE_NAME")
    service_endpoint = f"https://{service_name}.search.windows.net/"
    admin_key = os.getenv("ARXIV_SEARCH_ADMIN_KEY") 
    credential = AzureKeyCredential(admin_key)

    # Create a search index
    index_client = SearchClient(index_name=index_name,
        endpoint=service_endpoint, credential=credential)

    df = pd.read_json('ai_arxiv_202101.json', lines=True)

    count = 0
    documents = []
    for key, item in df.iterrows():

        count = count + 1

        if count % 1000 == 0:
            print(f"Processing record {count}")
        
        id = str(item["Id"])
        id = id.replace(".", "_")
        embeddings = await generate_embeddings(kernel, item["abstract"])
        # convert embeddings to a list of floats
        embeddings = [float(x) for x in embeddings]

        document = {
            "@search.action": "upload",
            "Id": id,
            "Text": item["title"],
            "Description": item["abstract"],
            "Embedding": embeddings
        }
        documents.append(document)

        # for every 100 records, upload them to the index
        if len(documents) == 100:
            result = index_client.upload_documents(documents)
            print(f"Uploaded {len(documents)} records")
            documents = []
    
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())