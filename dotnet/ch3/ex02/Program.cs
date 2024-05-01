using Microsoft.SemanticKernel;

async Task<string> CheckDocumentPart(Kernel kernel, string path, string part, string function)
{
    KernelPlugin documentPlugin = kernel.Plugins["ParseWordDocument"];
    KernelFunction documentParser = documentPlugin["ExtractTextUnderHeading"];
    KernelPlugin documentReader = kernel.Plugins["ProposalChecker"];
    
    var contextVariables = new KernelArguments
    {
        ["filePath"] = path,
        ["heading"] = part
    };
    // Check for text
    var text = await kernel.InvokeAsync(documentParser, contextVariables);

    var contextVariables2 = new KernelArguments
    {
        ["input"] = text.ToString(),
    };

    var result = await kernel.InvokeAsync(documentReader[function], contextVariables2);
    return result.ToString();
}

var (apiKey, orgId) = Settings.LoadFromFile();

Kernel kernel = Kernel.CreateBuilder()
                        .AddOpenAIChatCompletion("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt35")
                        .Build();

var checkerPlugin = kernel.ImportPluginFromObject(new Plugins.ProposalChecker.CheckSpreadsheet());
var documentParser = kernel.ImportPluginFromObject(new Plugins.ProposalChecker.ParseWordDocument());
var pluginPath = Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "..", "plugins", "ProposalChecker");
var documentReader = kernel.ImportPluginFromPromptDirectory(pluginPath, "ProposalChecker");


string data_directory = Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "..", "data", "proposals");


// Check for tabs
var result1 = await kernel.InvokeAsync(checkerPlugin["CheckValues"], new() {["filePath"] = $"{data_directory}/correct/correct.xlsx"});
var result2 = await kernel.InvokeAsync(checkerPlugin["CheckTabs"], new() {["filePath"] = $"{data_directory}/incorrect01/incorrect_template.xlsx"});
var result3 = await kernel.InvokeAsync(checkerPlugin["CheckValues"], new() {["filePath"] = $"{data_directory}/incorrect02/over_budget.xlsx"});
var result4 = await kernel.InvokeAsync(checkerPlugin["CheckValues"], new() {["filePath"] = $"{data_directory}/incorrect03/fast_increase.xlsx"});

// Console.WriteLine("Checking whether the correct tabs are present in the spreadsheet:");
// Console.WriteLine(result1);
// Console.WriteLine(result2);
// Console.WriteLine(result3);
// Console.WriteLine(result4);

// // Check for cells
// var result5 = await kernel.InvokeAsync(checkerPlugin["CheckCells"], new() {["filePath"] = $"{data_directory}/correct/correct.xlsx"});
// var result6 = await kernel.InvokeAsync(checkerPlugin["CheckCells"], new() {["filePath"] = $"{data_directory}/incorrect01/incorrect_template.xlsx"});
// var result7 = await kernel.InvokeAsync(checkerPlugin["CheckCells"], new() {["filePath"] = $"{data_directory}/incorrect02/over_budget.xlsx"});
// var result8 = await kernel.InvokeAsync(checkerPlugin["CheckCells"], new() {["filePath"] = $"{data_directory}/incorrect03/fast_increase.xlsx"});

// Console.WriteLine("Checking whether the correct cells are present in the spreadsheet:");
// Console.WriteLine(result5);
// Console.WriteLine(result6);
// Console.WriteLine(result7);
// Console.WriteLine(result8);

// // Check values
// var result9 = await kernel.InvokeAsync(checkerPlugin["CheckValues"], new() {["filePath"] = $"{data_directory}/correct/correct.xlsx"});
// var result10 = await kernel.InvokeAsync(checkerPlugin["CheckValues"], new() {["filePath"] = $"{data_directory}/incorrect02/over_budget.xlsx"});
// var result11 = await kernel.InvokeAsync(checkerPlugin["CheckValues"], new() {["filePath"] = $"{data_directory}/incorrect03/fast_increase.xlsx"});

// Console.WriteLine("Checking whether the correct values are present in the spreadsheet:");
// Console.WriteLine(result9);
// Console.WriteLine(result10);
// Console.WriteLine(result11);

var docPath1 = $"{data_directory}/correct/correct.docx";

string result_experience = CheckDocumentPart(kernel, docPath1, "Experience", "CheckExperience").Result;
string result_qualifications = CheckDocumentPart(kernel, docPath1, "Team", "CheckQualifications").Result;
string result_implementation = CheckDocumentPart(kernel, docPath1, "Implementation", "CheckImplementationDescription").Result;

Console.WriteLine($"Checking {docPath1}");
Console.WriteLine($"Experience: {result_experience}");
Console.WriteLine($"Qualifications: {result_qualifications}");
Console.WriteLine($"Implementation: {result_implementation}");
