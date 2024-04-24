using Microsoft.SemanticKernel;
using Plugins.ProposalChecker;
using System;
using System.IO;

var (apiKey, orgId) = Settings.LoadFromFile();

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4", apiKey, orgId);
builder.Plugins.AddFromPromptDirectory("../../../plugins/ProposalCheckerV2");
builder.Plugins.AddFromType<Helpers>();
builder.Plugins.AddFromType<ParseWordDocument>();
builder.Plugins.AddFromType<CheckSpreadsheet>();
var kernel = builder.Build();

KernelFunction processFolder = kernel.Plugins["Helpers"]["ProcessProposalFolder"];
KernelFunction checkTabs = kernel.Plugins["CheckSpreadsheet"]["CheckTabs"];
KernelFunction checkCells = kernel.Plugins["CheckSpreadsheet"]["CheckCells"];
KernelFunction checkValues = kernel.Plugins["CheckSpreadsheet"]["CheckValues"];
KernelFunction extractTeam = kernel.Plugins["ParseWordDocument"]["ExtractTeam"];
KernelFunction checkTeam = kernel.Plugins["ProposalCheckerV2"]["CheckTeamV2"];
KernelFunction extractExperience = kernel.Plugins["ParseWordDocument"]["ExtractExperience"];
KernelFunction checkExperience = kernel.Plugins["ProposalCheckerV2"]["CheckPreviousProjectV2"];
KernelFunction extractImplementation = kernel.Plugins["ParseWordDocument"]["ExtractImplementation"];
KernelFunction checkDates = kernel.Plugins["ProposalCheckerV2"]["CheckDatesV2"];

KernelFunction pipeline = KernelFunctionCombinators.Pipe(new[] {
    processFolder,
    checkTabs,
    checkCells,
    checkValues,
    extractTeam,
    checkTeam,
    extractExperience,
    checkExperience,
    extractImplementation,
    checkDates
}, "pipeline");


var proposals = Directory.GetDirectories("../../../data/proposals");

// print each directory
foreach (var proposal in proposals)
{
    // convert to absolute path
    string absolutePath = Path.GetFullPath(proposal);

    Console.WriteLine($"Processing {absolutePath}");
    KernelArguments context = new() { { "folderPath", absolutePath } };
    string ?result = await pipeline.InvokeAsync<string>(kernel, context); 
    Console.WriteLine(result);
    if (result == absolutePath) 
    {
        Console.WriteLine("Success!");
    }

    Console.WriteLine();
}
