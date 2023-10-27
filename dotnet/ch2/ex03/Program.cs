using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;

var builder = new KernelBuilder();
var (apiKey, orgId) = Settings.LoadFromFile();

builder.WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true);

IKernel kernel = builder.Build();

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins");

var promptPlugin = kernel.ImportSemanticSkillFromDirectory(pluginsDirectory, "prompt_engineering");

var problem = "When I was 6 my sister was half my age. Now I'm 70. How old is my sister?";

var chatFunctionVariables1 = new ContextVariables
{
    ["problem"] = problem,
};

var steps = await kernel.RunAsync(promptPlugin["solve_math_problem_v2"], chatFunctionVariables1);

Console.WriteLine(steps);

var chatFunctionVariables2 = new ContextVariables
{
    ["problem"] = problem,
    ["input"] = steps.ToString()
};

var result = await kernel.RunAsync(promptPlugin["chain_of_thought"], chatFunctionVariables2);

Console.WriteLine(result);