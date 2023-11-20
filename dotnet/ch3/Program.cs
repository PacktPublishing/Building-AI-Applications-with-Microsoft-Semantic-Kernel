using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;

async Task<string> CheckDocumentPart(IKernel kernel, string path, string part, string function)
{
    var documentParser = kernel.ImportFunctions(new Plugins.ProposalChecker.ParseWordDocument());
    var pluginPath = Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "plugins");
    var documentReader = kernel.ImportSemanticFunctionsFromDirectory(pluginPath, "ProposalChecker");

    var contextVariables = new ContextVariables
    {
        ["filePath"] = path,
        ["heading"] = part
    };
    // Check for text
    var text = await kernel.RunAsync(contextVariables, documentParser["ExtractTextUnderHeading"]);

    var contextVariables2 = new ContextVariables
    {
        ["input"] = text.ToString(),
    };

    var result = await kernel.RunAsync(contextVariables2, documentReader[function]);
    return result.ToString();
}

var (apiKey, orgId) = Settings.LoadFromFile();

IKernel kernel = new KernelBuilder()
    .WithOpenAIChatCompletionService("gpt-3.5-turbo", apiKey, orgId, serviceId: "gpt3", setAsDefault: true)
    .Build();
var data_directory = Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "data", "proposals");

var checkerPlugin = kernel.ImportFunctions(new Plugins.ProposalChecker.CheckSpreadsheet());

// Check for tabs
var result1 = await kernel.RunAsync($"{data_directory}/correct/correct.xlsx", checkerPlugin["CheckTabs"]);
var result2 = await kernel.RunAsync($"{data_directory}/incorrect1/incorrect_template.xlsx", checkerPlugin["CheckTabs"]);
var result3 = await kernel.RunAsync($"{data_directory}/incorrect2/over_budget.xlsx", checkerPlugin["CheckTabs"]);
var result4 = await kernel.RunAsync($"{data_directory}/incorrect3/fast_increase.xlsx", checkerPlugin["CheckTabs"]);

Console.WriteLine("Checking whether the correct tabs are present in the spreadsheet:");
Console.WriteLine(result1);
Console.WriteLine(result2);
Console.WriteLine(result3);
Console.WriteLine(result4);

// Check for cells
var result5 = await kernel.RunAsync($"{data_directory}/correct/correct.xlsx", checkerPlugin["CheckCells"]);
var result6 = await kernel.RunAsync($"{data_directory}/incorrect4/incorrect_cells.xlsx", checkerPlugin["CheckCells"]);
var result7 = await kernel.RunAsync($"{data_directory}/incorrect2/over_budget.xlsx", checkerPlugin["CheckCells"]);
var result8 = await kernel.RunAsync($"{data_directory}/incorrect3/fast_increase.xlsx", checkerPlugin["CheckCells"]);

Console.WriteLine("Checking whether the correct cells are present in the spreadsheet:");
Console.WriteLine(result5);
Console.WriteLine(result6);
Console.WriteLine(result7);
Console.WriteLine(result8);

// Check values
var result9 = await kernel.RunAsync($"{data_directory}/correct/correct.xlsx", checkerPlugin["CheckValues"]);
var result10 = await kernel.RunAsync($"{data_directory}/incorrect2/over_budget.xlsx", checkerPlugin["CheckValues"]);
var result11 = await kernel.RunAsync($"{data_directory}/incorrect3/fast_increase.xlsx", checkerPlugin["CheckValues"]);

Console.WriteLine("Checking whether the correct values are present in the spreadsheet:");
Console.WriteLine(result9);
Console.WriteLine(result10);
Console.WriteLine(result11);


var docPath2 = $"{data_directory}/incorrect1/missing_experience.docx";
var docPath3 = $"{data_directory}/incorrect2/missing_qualifications.docx";
var docPath4 = $"{data_directory}/incorrect3/missing_implementation_detail.docx";

var docPath1 = $"{data_directory}/correct/correct.docx";

string result_experience = CheckDocumentPart(kernel, docPath1, "Experience", "CheckExperience").Result;
string result_qualifications = CheckDocumentPart(kernel, docPath1, "Team", "CheckQualifications").Result;
string result_implementation = CheckDocumentPart(kernel, docPath1, "Implementation", "CheckImplementationDescription").Result;

Console.WriteLine($"Checking {docPath1}");
Console.WriteLine($"Experience: {result_experience}");
Console.WriteLine($"Qualifications: {result_qualifications}");
Console.WriteLine($"Implementation: {result_implementation}");
