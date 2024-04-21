using Microsoft.SemanticKernel;

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3")
                        .AddOpenAIChatCompletion("gpt-4", apiKey, orgId, serviceId: "gpt4")
                        .Build();

string prompt = "Finish the following knock-knock joke. Knock, knock. Who's there? {{$input}}, {{$input}} who?";
KernelFunction jokeFunction = kernel.CreateFunctionFromPrompt(prompt);
var arguments = new KernelArguments() { ["input"] = "Boo" };

var joke = await kernel.InvokeAsync(jokeFunction, arguments);

Console.WriteLine(joke);