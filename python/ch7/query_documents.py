import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai

from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.models import VectorizedQuery

from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt  
import pandas as pd
import os  

@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
async def generate_embeddings(kernel: sk.Kernel, text):
    e = await kernel.get_service("emb").generate_embeddings(text)
    # convert e[0] to a vector of floats
    result = [float(x) for x in e[0]]
    return result

def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    embedding_gen = sk_oai.OpenAITextEmbedding(service_id="emb", ai_model_id="text-embedding-3-small", api_key=api_key)
    kernel.add_service(embedding_gen)
    return kernel


async def main():
    kernel = create_kernel()
    
    ais_index_name = os.getenv("ARXIV_SEARCH_INDEX_NAME")
    ais_service_name = os.getenv("ARXIV_SEARCH_SERVICE_NAME")
    ais_service_endpoint = f"https://{ais_service_name}.search.windows.net/"
    ais_admin_key = os.getenv("ARXIV_SEARCH_ADMIN_KEY")
    credential = AzureKeyCredential(ais_admin_key)
        
    query_string = "models with long context windows lose information in the middle"

    search_client = SearchClient(ais_service_endpoint, ais_index_name, credential=credential)
    emb = await generate_embeddings(kernel, query_string)
    vector_query = VectorizedQuery(vector=emb, k_nearest_neighbors=5, exhaustive=True, fields="Embedding")
        
    results = search_client.search(  
        search_text=None,  
        vector_queries= [vector_query],
        select=["Id", "Text", "Description"]

    )  
    
    pd_results = []
    for result in results:
        d = {
            "id": result['Id'],
            "title": result['Description'],
            "abstract": result['Text'], 
            "score": f"{result['@search.score']:.2f}"
        }
        pd_results.append(d)
    pd_results = pd.DataFrame(pd_results)

    # print the title of each result
    i = 0
    for index, row in pd_results.iterrows():
        i = i + 1
        print(f"{i}. {row['title']}")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())