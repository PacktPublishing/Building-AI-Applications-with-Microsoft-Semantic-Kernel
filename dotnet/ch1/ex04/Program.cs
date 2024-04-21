using Microsoft.SemanticKernel;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3")
                        .AddOpenAIChatCompletion("gpt-4", apiKey, orgId, serviceId: "gpt4")
                        .Build();

var showManagerPlugin = kernel.ImportPluginFromObject(new Plugins.ShowManager());

var theme = await kernel.InvokeAsync(showManagerPlugin["RandomTheme"]);
Console.WriteLine("I will create a joke about " + theme);

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins", "jokes");


// Import the OrchestratorPlugin from the plugins directory.
var jokesPlugin = kernel.ImportPluginFromPromptDirectory(pluginsDirectory, "jokes");

var result = await kernel.InvokeAsync(jokesPlugin["knock_knock_joke"], new KernelArguments() {["input"] = theme.ToString()});

Console.WriteLine(result);

var explanation = await kernel.InvokeAsync(jokesPlugin["explain_joke"], new KernelArguments() {["input"] = result});

Console.WriteLine(explanation);