from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import os

class Helpers:

    @kernel_function(
        description="Checks that the folder contains the expected files, an Excel spreadsheet and a Word document",
        name="ProcessProposalFolder"
    )
    def ProcessProposalFolder(self, input: Annotated[str, "The file path to the folder containing the proposal files"]) -> str:
        xlsx_count = 0
        docx_count = 0

        for file in os.listdir(input):
            if file.lower().endswith(".xlsx"):
                xlsx_count += 1
            elif file.lower().endswith(".docx"):
                docx_count += 1
        
        return_value = "Error: unknown error"
        if xlsx_count == 1 and docx_count == 1:
            return_value = input
        elif xlsx_count == 0 and docx_count == 0:
            return_value = "Error: No files found"
        elif xlsx_count == 0:
            return_value = "Error: No Excel spreadsheet found"
        elif docx_count == 0:
            return_value =  "Error: No Word document found"
        else:
            return_value = "Error: multiple files found"

        return return_value
