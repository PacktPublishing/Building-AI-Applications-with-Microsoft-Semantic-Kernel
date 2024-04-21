using Microsoft.SemanticKernel;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3")
        .AddOpenAIChatCompletion("gpt-4", apiKey, orgId, serviceId: "gpt4")
                        .Build();



var showManagerPlugin = kernel.ImportPluginFromObject(new Plugins.ShowManager());

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins", "jokes");

var jokesPlugin = kernel.ImportPluginFromPromptDirectory(pluginsDirectory, "jokes");

var prompt = @"
$theme = {{ShowManager.RandomTheme}}

$joke = {{jokes.knock_knock_joke $theme}}

Here's the joke: $joke
";

var f = kernel.CreateFunctionFromPrompt(prompt);

var explanation = await kernel.InvokeAsync(f);

Console.WriteLine(explanation);