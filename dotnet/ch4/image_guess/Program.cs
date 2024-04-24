using Microsoft.SemanticKernel;
var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId);
builder.Plugins.AddFromPromptDirectory("../../../plugins/AnimalGuesser");
var kernel = builder.Build();

string clues = "Guess the animal from the following clues: It's a mammal, it's a pet, it barks.";
var guess = kernel.CreateFunctionFromPrompt(clues);

var animal_guess = await kernel.InvokeAsync(guess);
Console.WriteLine(animal_guess);
