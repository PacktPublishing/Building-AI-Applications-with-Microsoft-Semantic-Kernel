using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Plugins.Core;
#pragma warning disable SKEXP0003, SKEXP0011, SKEXP0052, SKEXP0050

var (apiKey, orgId) = Settings.LoadFromFile();
var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4-turbo-preview", apiKey, orgId);
var kernel = builder.Build();
kernel.ImportPluginFromObject(new ConversationSummaryPlugin());

const string prompt = @"
Chat history:
{{$history}}

User: {{$userInput}}
ChatBot:";

const string prompt2 = @"
Chat history:
{{ConversationSummaryPlugin.SummarizeConversation $history}}

User: {{$userInput}}
ChatBot:";

var executionSettings = new OpenAIPromptExecutionSettings {MaxTokens = 2000,Temperature = 0.8,};

var chatFunction = kernel.CreateFunctionFromPrompt(prompt2, executionSettings);
var history = "";
var arguments = new KernelArguments();
arguments["history"] = history;

var chatting = true;
while (chatting) {

    Console.Write("User: ");
    var input = Console.ReadLine();

    if (input == null) {break;}
    input = input.Trim();

    if (input == "exit") {break;}

    arguments["userInput"] = input;
    var answer = await chatFunction.InvokeAsync(kernel, arguments);
    var result = $"\nUser: {input}\nAssistant: {answer}\n";

    history += result;
    arguments["history"] = history;
    
    // Show the bot response
    Console.WriteLine(result);
}

Console.WriteLine("Goodbye!");