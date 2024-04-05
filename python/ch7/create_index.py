import os
from dotenv import load_dotenv
import os  
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents.indexes import SearchIndexClient  

from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    VectorSearch,  
    HnswAlgorithmConfiguration,
    HnswParameters,  
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    VectorSearchAlgorithmMetric,
)  

def main() -> None:

    index_name = "arxiv-papers-index"
    service_name = "ai-search-d-day"
    service_endpoint = f"https://{service_name}.search.windows.net/"
    admin_key = os.getenv("D_DAY_ADMIN_KEY")
    credential = AzureKeyCredential(admin_key)

    # Create a search index
    index_client = SearchIndexClient(
        endpoint=service_endpoint, credential=credential)
    
    index_client.delete_index(index_name)
    
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
        SearchableField(name="authors", type=SearchFieldDataType.String),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="abstract", type=SearchFieldDataType.String),
        SearchField(name="abstract_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=3072, vector_search_profile_name="myHnswProfile"),
    ]

    # Configure the vector search configuration  
    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="myHnsw",
                kind=VectorSearchAlgorithmKind.HNSW,
                parameters=HnswParameters(
                    m=4,
                    ef_construction=400,
                    ef_search=500,
                    metric=VectorSearchAlgorithmMetric.COSINE
                )
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="myHnswProfile",
                algorithm_configuration_name="myHnsw",
            )
        ]
    )

    # Create the search index with the semantic settings
    index = SearchIndex(name=index_name, fields=fields,
                        vector_search=vector_search)
    result = index_client.create_or_update_index(index)
    print(f' {result.name} created')

if __name__ == '__main__':
    load_dotenv()
    main()
