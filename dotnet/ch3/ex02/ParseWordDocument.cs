using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using System.ComponentModel;
using Microsoft.SemanticKernel;

namespace Plugins.ProposalChecker;
public class ParseWordDocument
{
    [KernelFunction, Description("Extracts the text under the heading in the Word document")]
    public static string ExtractTextUnderHeading(string filePath, string heading)
    {
        using (WordprocessingDocument doc = WordprocessingDocument.Open(filePath, false))
        {
            var body = doc.MainDocumentPart?.Document.Body;
            var paras = body?.Elements<Paragraph>();

            bool isExtracting = false;
            string extractedText = "";

            // if paras is null, return empty string
            if (paras == null)
            {
                return extractedText;
            }

            foreach (var para in paras)
            {
                if (para.ParagraphProperties != null &&
                    para.ParagraphProperties.ParagraphStyleId != null &&
                    para.ParagraphProperties.ParagraphStyleId.Val != null &&
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
                        para.ParagraphProperties.ParagraphStyleId.Val != null &&
                        para.ParagraphProperties.ParagraphStyleId.Val.Value == "Heading1")
                    {
                        break;
                    }

                    extractedText += para.InnerText + "\n";
                }
            }

            return extractedText.Trim();
        }
    }
}

