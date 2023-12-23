using Microsoft.SemanticKernel;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

public class Helpers
{
    [KernelFunction, Description("Checks that the folder contains one Word and one Excel file")]
    public static string ProcessProposalFolder([Description("Folder potentially containing")] string folderPath)
    {
        string result = folderPath;

        if (!Directory.Exists(folderPath))
        {
            return "Error: Folder does not exist";
        }

        var files = Directory.GetFiles(folderPath);
        int wordCount = files.Count(f => Path.GetExtension(f).ToLower() == ".docx");
        int excelCount = files.Count(f => Path.GetExtension(f).ToLower() == ".xlsx");

        if (wordCount == 1 && excelCount == 1)
        {
            return result;
        }
        else if (wordCount == 0 && excelCount == 0)
        {
            return "Error: Folder does not contain one Word and one Excel file";
        }
        else if (wordCount == 0)
        {
            return "Error: Folder missing Word file";
        }
        else if (excelCount == 0)
        {
            return "Error: Folder missing Excel file";
        }
        return "Error: Folder contains more than one Word or Excel file";

    }
}
