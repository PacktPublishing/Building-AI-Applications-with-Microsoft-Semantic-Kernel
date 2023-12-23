using Microsoft.SemanticKernel;
using Plugins;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.Plugins.AddFromType<Dalle3>();
builder.AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId);
var kernel = builder.Build();

KernelPlugin animalGuesser = kernel.ImportPluginFromPromptDirectory("../../../plugins/AnimalGuesser");
string clues = "It's a mammal. It's a pet. It meows. It purrs.";
KernelFunction guessAnimal = animalGuesser["GuessAnimal"];
KernelFunction generateImage = kernel.Plugins["Dalle3"]["ImageFromPrompt"];

KernelArguments context = new() { { "input", clues } };

KernelFunction pipeline = KernelFunctionCombinators.Pipe(new[]
{
    guessAnimal,
    generateImage
}, "pipeline");

Console.WriteLine(await pipeline.InvokeAsync(kernel, context));
