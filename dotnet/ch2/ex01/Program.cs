using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;

Console.WriteLine("Hello World!");

var builder = new KernelBuilder();
var (apiKey, orgId) = Settings.LoadFromFile();

builder.WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true);

IKernel kernel = builder.Build();

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins");

var promptPlugin = kernel.ImportSemanticFunctionsFromDirectory(pluginsDirectory, "prompt_engineering");

var chatFunctionVariables = new ContextVariables
{
    ["city"] = "New York City"
};

Console.WriteLine("Running prompt_engineering");
var result = await kernel.RunAsync(promptPlugin["attractions_single_variable"], chatFunctionVariables);

Console.WriteLine(result);