using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Planning.Handlebars;
#pragma warning disable SKEXP0060

var (apiKey, orgId) = Settings.LoadFromFile();
var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4", apiKey, orgId);
builder.Plugins.AddFromType<HomeAutomation>();
builder.Plugins.AddFromPromptDirectory("../../../plugins/MovieRecommender");
var kernel = builder.Build();

void FulfillRequest(HandlebarsPlanner planner, string ask)
{
    Console.WriteLine($"Fulfilling request: {ask}");
    var plan = planner.CreatePlanAsync(kernel, ask).Result;
    var result = plan.InvokeAsync(kernel, []).Result;
    Console.WriteLine("Request complete.");
}

var planner = new HandlebarsPlanner(new HandlebarsPlannerOptions() { AllowLoops = true });
FulfillRequest(planner, "Turn on the lights in the kitchen");
FulfillRequest(planner, "Open the windows of the bedroom, turn the lights off and put on Shawshank Redemption on the TV.");
FulfillRequest(planner, "Close the garage door and turn off the lights in all rooms.");
FulfillRequest(planner, "Turn off the lights in all rooms and play a movie in which Michael Keaton is a superhero in the bedroom.");
