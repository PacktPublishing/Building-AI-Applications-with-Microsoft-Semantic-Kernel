using Microsoft.SemanticKernel;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt35")
                        .Build();


var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(),
        "..", "..", "..", "plugins", "prompt_engineering");

var promptPlugin = kernel.ImportPluginFromPromptDirectory(pluginsDirectory, "prompt_engineering");

var function_arguments = new KernelArguments()
    {["city"] = "New York City",
    ["n_days"] = "3",
    ["likes"] = "restaurants, Ghostbusters, Friends tv show",
    ["dislikes"] = "museums, parks",
    ["n_attractions"] = "5"};

var result = await kernel.InvokeAsync(promptPlugin["attractions_multiple_variables"], function_arguments );

Console.WriteLine(result);