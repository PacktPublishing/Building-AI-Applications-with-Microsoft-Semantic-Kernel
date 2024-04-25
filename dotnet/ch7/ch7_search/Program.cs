
using Microsoft.SemanticKernel.Connectors.AzureAISearch;
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;

#pragma warning disable SKEXP0020
#pragma warning disable SKEXP0010
#pragma warning disable SKEXP0001
ISemanticTextMemory memoryWithCustomDb;

var (apiKey, orgId, searchServiceName, searchServiceAdminKey, searchIndexName) = Settings.LoadFromFile();

if (string.IsNullOrEmpty(apiKey) || string.IsNullOrEmpty(searchServiceName) || string.IsNullOrEmpty(searchServiceAdminKey) || string.IsNullOrEmpty(searchIndexName))
{
    Console.WriteLine("Configuration not found");
    return;
}

memoryWithCustomDb = new MemoryBuilder()
                .WithOpenAITextEmbeddingGeneration("text-embedding-3-small", apiKey)
                    .WithMemoryStore(new AzureAISearchMemoryStore(searchServiceName, searchServiceAdminKey))
                        .Build();

string query_string = "models with long context windows lose information in the middle";

IAsyncEnumerable<MemoryQueryResult> memories = memoryWithCustomDb.SearchAsync(searchIndexName, query_string, limit: 5, minRelevanceScore: 0.0);

int nResults = memories.CountAsync().Result;
Console.WriteLine($"Found {nResults} results");

int i = 0;
await foreach (MemoryQueryResult item in memories)
{
    i++;
    Console.WriteLine($"{i}. {item.Metadata.Description}");
}
