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

    [SKFunction, Description("Checks that each tab contains the cells A1-A5 and B1-B5 with the correct values")]
    public static string CheckCells(string filePath)
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
                foreach (var year in new[] { "2024", "2025" })
                {
                    var sheet = package.Workbook.Worksheets[year];
                    if (sheet.Cells["A1"].Text != "Quarter" || sheet.Cells["B1"].Text != "Budget" ||
                        sheet.Cells["A2"].Text != "Q1" || sheet.Cells["A3"].Text != "Q2" ||
                        sheet.Cells["A4"].Text != "Q3" || sheet.Cells["A5"].Text != "Q4")
                    {
                        return "Fail: missing quarters";
                    }
                    for (int row = 2; row <= 5; row++)
                    {
                        if (sheet.Cells[$"B{row}"].Value is not double)
                        {
                            return "Fail: non-numeric values";
                        }
                    }
                }
                return "Pass";
            }
        }
        catch (Exception ex)
        {
            return $"Fail: An error occurred: {ex.Message}";
        }
    }

    [SKFunction, Description("Check that the cells B2-B5 add to less than 1 million and don't increase over 10% each quarter")]
    public static string CheckValues(string filePath)
    {
        try
        {
            FileInfo fileInfo = new FileInfo(filePath);
            if (!fileInfo.Exists)
            {
                return "Fail: file does not exist.";
            }
            using (var package = new ExcelPackage(fileInfo))
            {
                foreach (var year in new[] { "2024", "2025" })
                {
                    var sheet = package.Workbook.Worksheets[year];
                    if (sheet == null)
                    {
                        return "Fail: Sheet for year {year} not found.";
                    }
                    double[] values = new double[4];
                    for (int i = 0; i < 4; i++)
                    {
                        if (sheet.Cells[i + 2, 2].Value is not double)
                        {
                            return $"Non-numeric value found in sheet {year}.";
                        }
                        else values[i] = (double)sheet.Cells[i + 2, 2].Value;
                    }
                    if (sum(values) >= 1000000)
                    {
                        return $"Sum of values in year {year} exceeds 1,000,000.";
                    }
                    for (int i = 0; i < values.Length - 1; i++)
                    {
                        if (values[i + 1] > values[i] * 1.10)
                        {
                            return $"More than 10% growth found from B{i+2} to B{i+3} in sheet {year}.";
                        }
                    }
                }
                return "Pass";
            }
        }
        catch (Exception ex)
        {
            return $"An error occurred: {ex.Message}";
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
