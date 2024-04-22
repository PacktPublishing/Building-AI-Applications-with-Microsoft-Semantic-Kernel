using Microsoft.SemanticKernel;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt35")
                        .Build();


var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(),
        "..", "..", "..", "plugins", "prompt_engineering");

var promptPlugin = kernel.ImportPluginFromPromptDirectory(pluginsDirectory, "prompt_engineering");

var problem = "When I was 6 my sister was half my age. Now I'm 70. How old is my sister?";

var chatFunctionVariables1 = new KernelArguments()
{
    ["problem"] = problem,
};

var steps = await kernel.InvokeAsync(promptPlugin["solve_math_problem_v2"], chatFunctionVariables1);

var chatFunctionVariables2 = new KernelArguments()
{
    ["problem"] = problem,
    ["input"] = steps.ToString()
};

var result = await kernel.InvokeAsync(promptPlugin["chain_of_thought_v2"], chatFunctionVariables2);

Console.WriteLine(result);