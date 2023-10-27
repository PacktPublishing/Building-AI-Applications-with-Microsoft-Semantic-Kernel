using System.Runtime.InteropServices;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.SemanticFunctions;

var builder = new KernelBuilder();

var (apiKey, orgId) = Settings.LoadFromFile();

builder.WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true);
builder.WithOpenAIChatCompletionService("gpt-4", apiKey, orgId, serviceId: "gpt4", setAsDefault: false);

IKernel kernel = builder.Build();

var showManagerPlugin = kernel.ImportSkill(new Plugins.ShowManager());

var theme = await kernel.RunAsync(showManagerPlugin["RandomTheme"]);
Console.WriteLine("I will create a joke about " + theme);

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins");

// Import the OrchestratorPlugin from the plugins directory.
var jokesPlugin = kernel.ImportSemanticSkillFromDirectory(pluginsDirectory, "jokes");

var result = await kernel.RunAsync(theme.ToString(), jokesPlugin["knock_knock_joke"]);

Console.WriteLine(result);

var explanation = await kernel.RunAsync(result.ToString(), jokesPlugin["explain_joke"]);

Console.WriteLine(explanation);