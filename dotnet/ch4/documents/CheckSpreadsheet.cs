using System.ComponentModel;
using Microsoft.SemanticKernel;
using OfficeOpenXml;

namespace Plugins.ProposalChecker;
public class CheckSpreadsheet
{
    [KernelFunction, Description("Checks that the spreadsheet contains the correct tabs, 2024 and 2025")]
    public string CheckTabs([Description("The file path to the spreadsheet")] string folderPath)
    {
        if (folderPath.StartsWith("Error"))
        {
            return folderPath;
        }
        string filePath = GetExcelFile(folderPath);
        try
        {
            FileInfo fileInfo = new FileInfo(filePath);

            if (!fileInfo.Exists)
            {
                return "Error: File does not exist.";
            }
            using (var package = new ExcelPackage(fileInfo))
            {
                ExcelPackage.LicenseContext = OfficeOpenXml.LicenseContext.NonCommercial;
                var workbook = package.Workbook;
                if (workbook.Worksheets.Count != 2)
                {
                    return "Error: Spreadsheet does not contain 2 tabs.";
                }
                if (workbook.Worksheets.Any(sheet => sheet.Name == "2024") && workbook.Worksheets.Any(sheet => sheet.Name == "2025"))
                {
                    return folderPath;
                }
                else
                {
                    return "Error: Spreadsheet does not contain 2024 and 2025 tabs.";
                }
            }
        }
        catch (Exception ex)
        {
            return $"Error: An error occurred: {ex.Message}";
        }
    }

    [KernelFunction, Description("Checks that each tab contains the cells A1-A5 and B1-B5 with the correct values")]
    public static string CheckCells(string folderPath)
    {
        if (folderPath.StartsWith("Error"))
        {
            return folderPath;
        }
        string filePath = GetExcelFile(folderPath);
        try 
        {    
            FileInfo fileInfo = new FileInfo(filePath);

            if (!fileInfo.Exists)
            {
                return "Error: File does not exist.";
            }        
            using (var package = new ExcelPackage(fileInfo))
            {
                foreach (var year in new[] { "2024", "2025" })
                {
                    var sheet = package.Workbook.Worksheets[year];
                    if (sheet.Cells["A1"].Text != "Quarter" || sheet.Cells["B1"].Text != "Budget" ||
                        sheet.Cells["A2"].Text != "Q1" || sheet.Cells["A3"].Text != "Q2" ||
                        sheet.Cells["A4"].Text != "Q3" || sheet.Cells["A5"].Text != "Q4")
                    {
                        return "Error: missing quarters";
                    }
                    for (int row = 2; row <= 5; row++)
                    {
                        if (sheet.Cells[$"B{row}"].Value is not double)
                        {
                            return "Error: non-numeric values";
                        }
                    }
                }
                return folderPath;
            }
        }
        catch (Exception ex)
        {
            return $"Error: An error occurred: {ex.Message}";
        }
    }

    [KernelFunction, Description("Check that the cells B2-B5 add to less than 1 million and don't increase over 10% each quarter")]
    public static string CheckValues(string folderPath)
    {
        if (folderPath.StartsWith("Error"))
        {
            return folderPath;
        }
        string filePath = GetExcelFile(folderPath);
        try
        {
            FileInfo fileInfo = new FileInfo(filePath);
            if (!fileInfo.Exists)
            {
                return "Error: file does not exist.";
            }
            using (var package = new ExcelPackage(fileInfo))
            {
                foreach (var year in new[] { "2024", "2025" })
                {
                    var sheet = package.Workbook.Worksheets[year];
                    if (sheet == null)
                    {
                        return "Error: Sheet for year {year} not found.";
                    }
                    double[] values = new double[4];
                    for (int i = 0; i < 4; i++)
                    {
                        if (sheet.Cells[i + 2, 2].Value is not double)
                        {
                            return $"Error: Non-numeric value found in sheet {year}.";
                        }
                        else values[i] = (double)sheet.Cells[i + 2, 2].Value;
                    }
                    if (sum(values) >= 1000000)
                    {
                        return $"Error: Sum of values in year {year} exceeds 1,000,000.";
                    }
                    for (int i = 0; i < values.Length - 1; i++)
                    {
                        if (values[i + 1] > values[i] * 1.10)
                        {
                            return $"Error: More than 10% growth found from B{i+2} to B{i+3} in sheet {year}.";
                        }
                    }
                }
                return folderPath;
            }
        }
        catch (Exception ex)
        {
            return $"Error: An error occurred: {ex.Message}";
        }
    }

    private static string GetExcelFile(string folderPath)
    {
        if (folderPath.StartsWith("Error"))
        {
            return folderPath;
        }
        try
        {
            var files = Directory.GetFiles(folderPath);
            var excelFiles = files.Where(f => Path.GetExtension(f).ToLower() == ".xlsx");
            return excelFiles.First();
        }
        catch (Exception ex)
        {
            return $"Error: {ex.Message}";
        }
    }
    static double sum(double[] values)
    {
        double total = 0;
        foreach (var value in values)
        {
            total += value;
        }
        return total;
    }

}
