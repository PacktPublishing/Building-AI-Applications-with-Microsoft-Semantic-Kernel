
using Microsoft.SemanticKernel.Connectors.AzureAISearch;
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using System.Text.Json;


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

// Configure the builder to use OpenAI's Text Embedding API and Azure Cognitive Search
memoryWithCustomDb = new MemoryBuilder()
                .WithOpenAITextEmbeddingGeneration("text-embedding-3-small", apiKey)
                    .WithMemoryStore(new AzureAISearchMemoryStore(searchServiceName, searchServiceAdminKey))
                        .Build();

// read the text file ai_arxiv_short.json
string data = File.ReadAllText("ai_arxiv.json");

int i = 0;
// for each line in the file
foreach (string line in data.Split('\n'))
{
    i++;
    if (i < 2000) continue;

    var paper = JsonSerializer.Deserialize<Dictionary<string, object>>(line);

    if (paper == null)
    {
        continue;
    }

    string title = paper["title"]?.ToString() ?? "No title available";
    string id = paper["id"]?.ToString() ?? "No ID available";
    string abstractText = paper["abstract"]?.ToString() ?? "No abstract available";

    // in id, replace . with _
    id = id.Replace(".", "_");


    await memoryWithCustomDb.SaveInformationAsync(collection: searchIndexName,
        text: abstractText,
        id: id,
        description: title);
        

    if (i % 100 == 0)
    {
        Console.WriteLine($"Processed {i} documents at {DateTime.Now}");
    }
}



