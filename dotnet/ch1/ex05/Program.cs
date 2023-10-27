using Microsoft.SemanticKernel;

var builder = new KernelBuilder();
var (apiKey, orgId) = Settings.LoadFromFile();

builder.WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true);
builder.WithOpenAIChatCompletionService("gpt-4", apiKey, orgId, serviceId: "gpt4", setAsDefault: false);

IKernel kernel = builder.Build();

var showManagerPlugin = kernel.ImportSkill(new Plugins.ShowManager());

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins");

var jokesPlugin = kernel.ImportSemanticSkillFromDirectory(pluginsDirectory, "jokes");

var explanation = await kernel.RunAsync(
        showManagerPlugin["RandomTheme"], 
        jokesPlugin["knock_knock_joke"],
        jokesPlugin["explain_joke"]);

Console.WriteLine(explanation);