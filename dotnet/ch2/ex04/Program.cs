using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;
using Microsoft.SemanticKernel.SemanticFunctions;

var builder = new KernelBuilder();
var (apiKey, orgId) = Settings.LoadFromFile();

builder.WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true);

IKernel kernel = builder.Build();

var pluginsDirectory = Path.Combine(System.IO.Directory.GetCurrentDirectory(), 
        "..", "..", "..", "plugins");

var promptPlugin = kernel.ImportSemanticSkillFromDirectory(pluginsDirectory, "prompt_engineering");

var problem = "When I was 6 my sister was half my age. Now I'm 70. How old is my sister?";

// create a list of integers
var results = new List<int>();

// call the program 5 times
for (int i = 0; i < 5; i++)
{

    var chatFunctionVariables1 = new ContextVariables
    {
        ["problem"] = problem,
    };

    var steps = await kernel.RunAsync(promptPlugin["solve_math_problem_v2"], chatFunctionVariables1);

    var chatFunctionVariables2 = new ContextVariables
    {
        ["problem"] = problem,
        ["input"] = steps.ToString()
    };

    // run the program
    var result = await kernel.RunAsync(promptPlugin["chain_of_thought_v2"], chatFunctionVariables2);

    // convert the result to an integer
    var resultInt = int.Parse(result.ToString());

    // add the result to the list
    results.Add(resultInt);
}

// Find the most common result
var mostCommonResult = results.GroupBy(x => x)
    .OrderByDescending(x => x.Count())
    .First()
    .Key;

Console.WriteLine($"Your sister's age is {mostCommonResult}");