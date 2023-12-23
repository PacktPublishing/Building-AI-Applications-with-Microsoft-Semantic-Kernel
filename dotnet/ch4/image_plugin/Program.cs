using Microsoft.SemanticKernel;
using Plugins;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.Plugins.AddFromType<Dalle3>();
var kernel = builder.Build();

string prompt = "A cat sitting on a couch in the style of Monet"; 
string? url = await kernel.InvokeAsync<string>(
    "Dalle3", "ImageFromPrompt", new() {{ "prompt", prompt }}
);

Console.Write(url);
