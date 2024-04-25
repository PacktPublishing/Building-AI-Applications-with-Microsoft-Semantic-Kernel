using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;


var (apiKey, orgId, searchServiceName, searchServiceAdminKey, searchIndexName) = Settings.LoadFromFile();

if (string.IsNullOrEmpty(apiKey) || string.IsNullOrEmpty(searchServiceName) || string.IsNullOrEmpty(searchServiceAdminKey) || string.IsNullOrEmpty(searchIndexName))
{
    Console.WriteLine("Configuration not found");
    return;
}

// Load environment variables
string indexName = "arxiv-papers-index-csharp";
string serviceEndpoint = searchServiceName; 
string adminKey = searchServiceAdminKey;
AzureKeyCredential credential = new AzureKeyCredential(adminKey);

// Create a search index client
SearchIndexClient indexClient = new SearchIndexClient(new Uri(serviceEndpoint), credential);

// Delete the existing index
indexClient.DeleteIndex(indexName);

// Define fields for the search index
var fields = new FieldBuilder().Build(typeof(SearchModel));

// Create the search index with the semantic settings
SearchIndex index = new SearchIndex(indexName)
{
    Fields = fields,
    // Add vector search configuration if needed
};

// Create or update the index
var result = indexClient.CreateOrUpdateIndex(index);
Console.WriteLine($"{result}");
