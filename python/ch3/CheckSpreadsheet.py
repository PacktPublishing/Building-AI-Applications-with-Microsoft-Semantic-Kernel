import openpyxl
from semantic_kernel.skill_definition import sk_function

class CheckSpreadsheet:

    @sk_function(
        description="Checks that the spreadsheet contains the correct tabs, 2024 and 2025",
        name="CheckTabs",
        input_description="The file path to the spreadsheet",
    )
    def check_tabs(self, path: str) -> str:
        try:
            workbook = openpyxl.load_workbook(path)
            sheet_names = workbook.sheetnames
            if sheet_names == ['2024', '2025']:
                return "Pass"
            else:
                return "Fail: the spreadsheet does not contain the correct tabs"
        except Exception as e:
            return f"Fail: an exception {e} occurred when trying to open the spreadsheet"
            