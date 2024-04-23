from docx import Document
from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class ParseWordDocument:

    @kernel_function(
        description="Extract the text under the given heading",
        name="ExtractTextUnderHeading",
    )

    async def ExtractTextUnderHeading(self, 
            doc_path: Annotated[str, "The path for the file we want to evaluate"],
            target_heading: Annotated[str, "The heading we want to extract the text from"]
            ) -> Annotated[str, "The extracted text"]:
        doc = Document(str(doc_path))
        extract = False
        extracted_text = ''

        for paragraph in doc.paragraphs:
            if paragraph.style.name == 'Heading 1':
                if extract:
                    break  # Stop if next heading is found
                extract = paragraph.text.strip().lower() == str(target_heading).lower()
            elif extract:
                extracted_text += paragraph.text + '\n'

        return extracted_text.strip()
