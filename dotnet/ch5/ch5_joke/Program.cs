using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4", apiKey, orgId);
builder.Plugins.AddFromPromptDirectory("../../../plugins/jokes");
var kernel = builder.Build();

var planner = new HandlebarsPlanner(new HandlebarsPlannerOptions() { AllowLoops = true });
var ask = "Create four knock-knock jokes: two about dogs, one about cats and one about ducks. Don't explain the jokes, just write them.";
var plan = await planner.CreatePlanAsync(kernel, ask);
var result = (await plan.InvokeAsync(kernel, [])).Trim();
Console.Write ($"Results: {result}");
