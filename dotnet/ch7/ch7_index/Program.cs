using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel.Plugins.Memory;
using Microsoft.SemanticKernel.Connectors.OpenAI;

#pragma warning disable SKEXP0003, SKEXP0011, SKEXP0052

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4-turbo-preview", apiKey, orgId);
var kernel = builder.Build();

var memoryBuilder = new MemoryBuilder();
memoryBuilder.WithMemoryStore(new VolatileMemoryStore());
memoryBuilder.WithOpenAITextEmbeddingGeneration("text-embedding-3-small", apiKey);
var memory = memoryBuilder.Build();

const string MemoryCollectionName = "default";
await memory.SaveInformationAsync(MemoryCollectionName, id: "1", text: "My favorite city is Paris");
await memory.SaveInformationAsync(MemoryCollectionName, id: "2", text: "My favorite activity is visiting museums");

kernel.ImportPluginFromObject(new TextMemoryPlugin(memory));
const string prompt = @"
Information about me, from previous conversations:
- {{$city}} {{recall $city}}
- {{$activity}} {{recall $activity}}

Generate a personalized tour of activities for me to do when I have a free day in my favorite city. I just want to do my favorite activity.
";

var f = kernel.CreateFunctionFromPrompt(prompt, new OpenAIPromptExecutionSettings { MaxTokens = 2000, Temperature = 0.8 });
var context = new KernelArguments();
context["city"] = "What is my favorite city?";
context["activity"] = "What is my favorite activity?";

context[TextMemoryPlugin.CollectionParam] = MemoryCollectionName;
context[TextMemoryPlugin.LimitParam] = "2";
context[TextMemoryPlugin.RelevanceParam] = "0.6";

var result = await f.InvokeAsync(kernel, context);
Console.WriteLine(result);