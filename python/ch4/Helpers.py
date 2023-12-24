from semantic_kernel.skill_definition import sk_function
import os

class Helpers:

    @sk_function(
        description="Checks that the folder contains the expected files, an Excel spreadsheet and a Word document",
        name="ProcessProposalFolder",
        input_description="The file path to the folder containing the proposal files",
    )
    def ProcessProposalFolder(self, folder_path: str) -> str:
        xlsx_count = 0
        docx_count = 0

        for file in os.listdir(folder_path):
            if file.lower().endswith(".xlsx"):
                xlsx_count += 1
            elif file.lower().endswith(".docx"):
                docx_count += 1
        
        return_value = "Error: unknown error"
        if xlsx_count == 1 and docx_count == 1:
            return_value = folder_path
        elif xlsx_count == 0 and docx_count == 0:
            return_value = "Error: No files found"
        elif xlsx_count == 0:
            return_value = "Error: No Excel spreadsheet found"
        elif docx_count == 0:
            return_value =  "Error: No Word document found"
        else:
            return_value = "Error: multiple files found"

        return return_value
