
using Microsoft.SemanticKernel.Connectors.AzureAISearch;
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using System.Data.Common;

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

string input = "";
int i = 0;
await foreach (MemoryQueryResult item in memories)
{
    i++;
    input += $"{i}. {item.Metadata.Text}";
}

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-4-turbo", apiKey, orgId, serviceId: "gpt-4-turbo")
                        .Build();

// Import the OrchestratorPlugin from the plugins directory.
var rag = kernel.ImportPluginFromPromptDirectory("prompts", "SummarizeAbstract");

string explanation = "Here are the top 5 documents that are most like your query:\n";
int j = 0;
await foreach (MemoryQueryResult item in memories)
{
    j++;
    string id = item.Metadata.Id;
    id.Replace('_', '.');
    explanation += $"{j}. {item.Metadata.Description}\n";
    explanation += $"https://arxiv.org/abs/{id}\n";
}
explanation += "\n";

explanation += await kernel.InvokeAsync(rag["summarize_abstracts"], new KernelArguments() {["input"] = input});

Console.WriteLine(explanation);