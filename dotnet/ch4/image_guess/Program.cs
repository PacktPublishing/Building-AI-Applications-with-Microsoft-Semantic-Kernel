using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Plugins;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.Plugins.AddFromType<Dalle3>();
builder.AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId);
builder.Plugins.AddFromPromptDirectory("../../../plugins/AnimalGuesser");
var kernel = builder.Build();

OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
{
    ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
};

string clues = "Guess the animal from the following clues: It's a mammal, it's a pet, it barks.";
var guess = kernel.CreateFunctionFromPrompt(clues, openAIPromptExecutionSettings);

var animal_guess = await kernel.InvokeAsync(guess);
Console.WriteLine(animal_guess);

string image_prompt = "Generate a DALLE-3 image of a falcon flying on a beach";
var gen = kernel.CreateFunctionFromPrompt(image_prompt, openAIPromptExecutionSettings); 
var image_url = await kernel.InvokeAsync(gen);
Console.WriteLine(image_url);