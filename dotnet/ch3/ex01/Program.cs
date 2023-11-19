using Microsoft.SemanticKernel;
using System.IO;

var (apiKey, orgId) = Settings.LoadFromFile();

IKernel kernel = new KernelBuilder()
    .WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true)
    .Build();

var checkerPlugin = kernel.ImportFunctions(new Plugins.ProposalChecker.CheckSpreadsheet());
var data_directory = Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "..", "data", "proposals");
var result1 = await kernel.RunAsync($"{data_directory}/correct/correct.xlsx", checkerPlugin["CheckTabs"]);
Console.WriteLine(result1);
var result2 = await kernel.RunAsync($"{data_directory}/incorrect1/incorrect_template.xlsx", checkerPlugin["CheckTabs"]);
Console.WriteLine(result2);