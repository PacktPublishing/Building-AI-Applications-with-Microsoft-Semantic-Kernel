from docx import Document
from semantic_kernel.skill_definition import sk_function
import os

class ParseWordDocument:

    @sk_function(
        description="Extracts information about the team",
        name="ExtractTeam",
        input_description="The file path to the Word document",
    )
    def ExtractTeam(self, folder_path: str) -> str:
        if folder_path.startswith("Error"):
            return folder_path
        doc_path = self.get_first_docx_file(folder_path)
        text = self.ExtractTextUnderHeading(doc_path, 'Team')
        return f"FolderPath: {folder_path}\n{text}"

    @sk_function(
        description="Extracts information about the team's experience on their previous project",
        name="ExtractExperience",
        input_description="The file path to the Word document",
    )
    def ExtractExperience(self, folder_path: str) -> str:
        if folder_path.startswith("Error"):
            return folder_path
        doc_path = self.get_first_docx_file(folder_path)
        text =  self.ExtractTextUnderHeading(doc_path, 'Experience')
        return f"FolderPath: {folder_path}\n{text}"
    
    @sk_function(
        description="Extracts information about the implementation plan being proposed",
        name="ExtractImplementation",
        input_description="The file path to the Word document",
    )
    def ExtractImplementation(self, folder_path: str) -> str:
        if folder_path.startswith("Error"):
            return folder_path
        doc_path = self.get_first_docx_file(folder_path)
        text = self.ExtractTextUnderHeading(doc_path, 'Implementation')
        return f"FolderPath: {folder_path}\n{text}"

    def get_first_docx_file(self, folder_path: str) -> str:
        if folder_path.startswith("FolderPath"):
            folder_path = folder_path.split(":")[1].strip()
        if folder_path.startswith("Error"):
            return folder_path
        for file in os.listdir(folder_path):
            if file.endswith(".docx"):
                return os.path.join(folder_path, file)

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
