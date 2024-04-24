from docx import Document
from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import os

class ParseWordDocument:

    @kernel_function(
        description="Extracts information about the team",
        name="ExtractTeam",
    )
    def ExtractTeam(self,
                    input: Annotated[str, "The path of the file to extract the text from"]) ->  \
                    Annotated[str, "The extracted text about the team description text"]:                    
        if input.startswith("Error"):
            return input
        doc_path = self.get_first_docx_file(input)
        text = self.ExtractTextUnderHeading(doc_path, 'Team')
        return f"FolderPath: {input}\n{text}"

    @kernel_function(
        description="Extracts information about the team's experience on their previous project",
        name="ExtractExperience",
    )
    def ExtractExperience(self,
                              input: Annotated[str, "The path of the file to extract the text from"]) ->  \
                              Annotated[str, "The extracted experience text"]:                          
        if input.startswith("Error"):
            return input
        doc_path = self.get_first_docx_file(input)
        text =  self.ExtractTextUnderHeading(doc_path, 'Experience')
        return f"FolderPath: {input}\n{text}"
    
    @kernel_function(
        description="Extracts information about the implementation plan being proposed",
        name="ExtractImplementation",
    )
    def ExtractImplementation(self, 
                              input: Annotated[str, "The path of the file to extract the text from"]) ->  \
                              Annotated[str, "The extracted implementation text"]:
        if input.startswith("Error"):
            return input
        doc_path = self.get_first_docx_file(input)
        text = self.ExtractTextUnderHeading(doc_path, 'Implementation')
        return f"FolderPath: {input}\n{text}"

    def get_first_docx_file(self, input: str) -> str:
        if input.startswith("FolderPath"):
            input = input.split(":")[1].strip()
        if input.startswith("Error"):
            return input
        for file in os.listdir(input):
            if file.endswith(".docx"):
                return os.path.join(input, file)

    def ExtractTextUnderHeading(self, doc_path: str, target_heading: str) -> str:
        doc = Document(doc_path)
        extract = False
        extracted_text = ''

        for paragraph in doc.paragraphs:
            if paragraph.style.name == 'Heading 1':
                if extract:
                    break  # Stop if next heading is found
                extract = paragraph.text.strip().lower() == target_heading.lower()
            elif extract:
                extracted_text += paragraph.text + '\n'
        return extracted_text.strip()
