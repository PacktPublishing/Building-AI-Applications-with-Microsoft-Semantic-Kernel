using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning;

var builder = new KernelBuilder();
var (apiKey, orgId) = Settings.LoadFromFile();

builder.WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true);
builder.WithOpenAIChatCompletionService("gpt-4", apiKey, orgId, serviceId: "gpt4", setAsDefault: false);

IKernel kernel = builder.Build();

var showManagerPlugin = kernel.ImportSkill(new Plugins.ShowManager());

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins");

var jokesPlugin = kernel.ImportSemanticSkillFromDirectory(pluginsDirectory, "jokes");

var planner = new SequentialPlanner(kernel);
var ask = "Choose a random theme for a joke, generate a knock-knock joke about it and explain it";
var plan = await planner.CreatePlanAsync(ask);
Console.WriteLine(plan.ToSafePlanString());

var joke_and_explanation = plan.InvokeAsync();
Console.WriteLine(joke_and_explanation.Result);