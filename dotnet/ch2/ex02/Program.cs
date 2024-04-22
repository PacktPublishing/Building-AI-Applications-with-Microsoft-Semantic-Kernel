using Microsoft.SemanticKernel;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt35")
                        .Build();


var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins", "prompt_engineering");

var promptPlugin = kernel.ImportPluginFromPromptDirectory(pluginsDirectory, "prompt_engineering");
var result = await kernel.InvokeAsync(promptPlugin["attractions_single_variable_v2"], new KernelArguments() {["city"] = "New York City"});

Console.WriteLine(result);