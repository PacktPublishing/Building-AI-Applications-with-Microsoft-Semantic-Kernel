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

    index_name = os.getenv("ARXIV_SEARCH_INDEX_NAME")
    service_name = os.getenv("ARXIV_SEARCH_SERVICE_NAME")
    service_endpoint = f"https://{service_name}.search.windows.net/"
    admin_key = os.getenv("ARXIV_SEARCH_ADMIN_KEY")
    credential = AzureKeyCredential(admin_key)

    # Create a search index
    index_client = SearchIndexClient(
        endpoint=service_endpoint, credential=credential)
    
    index_client.delete_index(index_name)
    
    fields = [
        SimpleField(name="Id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
        SearchableField(name="AdditionalMetadata", type=SearchFieldDataType.String),
        SearchableField(name="Text", type=SearchFieldDataType.String),
        SearchableField(name="Description", type=SearchFieldDataType.String),
        SearchableField(name="ExternalSourceName", type=SearchFieldDataType.String),
        SimpleField(name="IsReference", type=SearchFieldDataType.Boolean),
        SearchField(name="Embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile"),
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
    result = index_client.create_or_update_index(index, all)
    print(f' {result.name} created')

if __name__ == '__main__':
    load_dotenv()
    main()
