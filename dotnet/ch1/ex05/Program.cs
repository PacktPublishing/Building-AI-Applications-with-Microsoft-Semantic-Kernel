#pragma warning disable SKEXP0060

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3")
        .AddOpenAIChatCompletion("gpt-4", apiKey, orgId, serviceId: "gpt4")
                        .Build();


var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(),
        "..", "..", "..", "plugins", "jokes");

kernel.ImportPluginFromPromptDirectory(pluginsDirectory);

var goalFromUser = "Choose a random theme for a joke, generate a knock-knock joke about it and explain it"; 

var planner = new HandlebarsPlanner(new HandlebarsPlannerOptions() { AllowLoops = false });
var plan = await planner.CreatePlanAsync(kernel, goalFromUser);

// Execute the plan
var result = await plan.InvokeAsync(kernel);

// Print the result to the console
Console.WriteLine(result);
