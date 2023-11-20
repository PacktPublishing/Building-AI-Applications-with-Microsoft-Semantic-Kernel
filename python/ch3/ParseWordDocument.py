from docx import Document
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext

class ParseWordDocument:

    @sk_function(
        description="Extract the text under the given heading",
        name="ExtractTextUnderHeading",
        input_description="The file path to the Word document",
    )
    @sk_function_context_parameter(
        name="doc_path",
        description="The file path",
    )
    @sk_function_context_parameter(
        name="target_heading",
        description="The name of the heading that we want to extract the text",
    )        
    def ExtractTextUnderHeading(self, context: SKContext) -> str:
        doc = Document(str(context['doc_path']))
        extract = False
        extracted_text = ''

        for paragraph in doc.paragraphs:
            if paragraph.style.name == 'Heading 1':
                if extract:
                    break  # Stop if next heading is found
                extract = paragraph.text.strip().lower() == str(context['target_heading']).lower()
            elif extract:
                extracted_text += paragraph.text + '\n'

        return extracted_text.strip()
