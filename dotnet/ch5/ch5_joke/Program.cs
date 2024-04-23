#pragma warning disable SKEXP0060

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;
using Microsoft.SemanticKernel.Connectors.OpenAI;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4", apiKey, orgId);
var kernel = builder.Build();

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(),
        "..", "..", "..", "plugins", "jokes");

kernel.ImportPluginFromPromptDirectory(pluginsDirectory);

var plannerOptions = new HandlebarsPlannerOptions()
    {
        ExecutionSettings = new OpenAIPromptExecutionSettings()
        {
            Temperature = 0.0,
            TopP = 0.1,
            MaxTokens = 4000
        },
        AllowLoops = true
    };

var planner = new HandlebarsPlanner(plannerOptions);
var ask = "Tell four knock-knock jokes: two about dogs, one about cats and one about ducks";
var plan = await planner.CreatePlanAsync(kernel, ask);
var result = await plan.InvokeAsync(kernel);
Console.Write ($"Results: {result}");
