using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using System.ComponentModel;
using Microsoft.SemanticKernel;
namespace Plugins.ProposalChecker;
public class ParseWordDocument
{

    [KernelFunction, Description("Extracts the text under the Team heading in the Word document")]
    public static string ExtractTeam(string folderPath)
    {
        return ExtractTextUnderHeading(folderPath, "Team");
    }

    [KernelFunction, Description("Extracts the text under the Experience heading in the Word document")]
    public static string ExtractExperience(string folderPath)
    {
        return ExtractTextUnderHeading(folderPath, "Experience");
    }

    [KernelFunction, Description("Extracts the text under the Implementation heading in the Word document")]
    public static string ExtractImplementation(string folderPath)
    {
        return ExtractTextUnderHeading(folderPath, "Implementation");
    }

    private static string ExtractTextUnderHeading(string folderPath, string heading)
    {
        if (folderPath.Contains("Error"))
        {
            return folderPath;
        }
        if (folderPath.StartsWith("FolderPath:"))
        {
            folderPath = folderPath.Substring("FolderPath: ".Length);
            folderPath = folderPath.Trim();
        }
        string filePath = Directory.GetFiles(folderPath).First(f => Path.GetExtension(f).ToLower() == ".docx");

        using (WordprocessingDocument doc = WordprocessingDocument.Open(filePath, false))
        {
            var body = doc.MainDocumentPart.Document.Body;
            var paras = body.Elements<Paragraph>();

            bool isExtracting = false;
            string extractedText = "";

            foreach (var para in paras)
            {
                if (para.ParagraphProperties != null &&
                    para.ParagraphProperties.ParagraphStyleId != null &&
                    para.ParagraphProperties.ParagraphStyleId.Val.Value == "Heading1" &&
                    para.InnerText.Trim().Equals(heading, StringComparison.OrdinalIgnoreCase))
                {
                    isExtracting = true;
                    continue;
                }

                if (isExtracting)
                {
                    if (para.ParagraphProperties != null &&
                        para.ParagraphProperties.ParagraphStyleId != null &&
                        para.ParagraphProperties.ParagraphStyleId.Val.Value == "Heading1")
                    {
                        break;
                    }

                    extractedText += para.InnerText + "\n";
                }
            }

            if (extractedText == "")
            {
                return $"Error: Missing section {heading}";
            }

            return $"FolderPath: {folderPath}\n"  + extractedText.Trim();
        }
    }
}

