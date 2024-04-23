# pragma warning disable SKEXP0050

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Plugins.Core;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt35");
builder.Plugins.AddFromType<TimePlugin>(pluginName: "time");
Kernel kernel = builder.Build();

const string promptTemplate = @"
Today is: {{time.date}}
Current time is: {{time.time}}

Answer to the following questions using JSON syntax, including the data used.
Is it morning, afternoon, evening, or night (morning/afternoon/evening/night)?
Is it weekend time (weekend/not weekend)?";

var results = await kernel.InvokePromptAsync(promptTemplate);
Console.WriteLine(results);
