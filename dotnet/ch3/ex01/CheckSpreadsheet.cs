using System.ComponentModel;
using System.Globalization;
using Microsoft.SemanticKernel;
using OfficeOpenXml;

namespace Plugins.ProposalChecker;
public class CheckSpreadsheet
{
    [SKFunction, Description("Checks that the spreadsheet contains the correct tabs, 2024 and 2025")]
    public string CheckTabs([Description("The file path to the spreadsheet")] string filePath)
    {
        try
        {
            FileInfo fileInfo = new FileInfo(filePath);

            if (!fileInfo.Exists)
            {
                return "Fail: File does not exist.";
            }
            using (var package = new ExcelPackage(fileInfo))
            {
                ExcelPackage.LicenseContext = OfficeOpenXml.LicenseContext.NonCommercial;
                var workbook = package.Workbook;
                if (workbook.Worksheets.Count != 2)
                {
                    return "Fail: Spreadsheet does not contain 2 tabs.";
                }
                if (workbook.Worksheets.Any(sheet => sheet.Name == "2024") && workbook.Worksheets.Any(sheet => sheet.Name == "2025"))
                {
                    return "Pass";
                }
                else
                {
                    return "Fail: Spreadsheet does not contain 2024 and 2025 tabs.";
                }
            }
        }
        catch (Exception ex)
        {
            return $"Fail: An error occurred: {ex.Message}";
        }
    }
}
