import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from CheckSpreadsheet import CheckSpreadsheet
from ParseWordDocument import ParseWordDocument


async def run_spreadsheet_check(path, function):
    kernel = sk.Kernel()
    
    check_spreadsheet = kernel.import_skill(CheckSpreadsheet())

    result = await kernel.run_async(
        check_spreadsheet[function],
        input_str=path,
    )
    print(result)


async def run_document_check(path, function, target_heading, semantic_function):
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)
    kernel.add_chat_service("gpt35", gpt35)

    parse_word_document = kernel.import_skill(ParseWordDocument())

    variables = sk.ContextVariables()
    variables['doc_path'] = path
    variables['target_heading'] = target_heading

    text = await kernel.run_async(
        parse_word_document[function],
        input_vars=variables
    )

    check_docs = kernel.import_semantic_skill_from_directory("../plugins", "ProposalChecker")
    result = check_docs[semantic_function](str(text))
    print(f"{target_heading}: {result}")

async def main():
    data_path = "../data/proposals/"
    await run_spreadsheet_check(f"{data_path}/correct/correct.xlsx", "CheckTabs")
    await run_spreadsheet_check(f"{data_path}/incorrect1/incorrect_template.xlsx", "CheckTabs")
    await run_spreadsheet_check(f"{data_path}/incorrect2/over_budget.xlsx", "CheckTabs")
    await run_spreadsheet_check(f"{data_path}/incorrect3/fast_increase.xlsx", "CheckTabs")
    
    await run_spreadsheet_check(f"{data_path}/correct/correct.xlsx", "CheckCells")
    await run_spreadsheet_check(f"{data_path}/incorrect4/incorrect_cells.xlsx", "CheckCells")
    await run_spreadsheet_check(f"{data_path}/incorrect2/over_budget.xlsx", "CheckCells")
    await run_spreadsheet_check(f"{data_path}/incorrect3/fast_increase.xlsx", "CheckCells")

    await run_spreadsheet_check(f"{data_path}/correct/correct.xlsx", "CheckValues")
    await run_spreadsheet_check(f"{data_path}/incorrect2/over_budget.xlsx", "CheckValues")
    await run_spreadsheet_check(f"{data_path}/incorrect3/fast_increase.xlsx", "CheckValues")

    print("Word document checks:")

    await run_document_check(f"{data_path}/correct/correct.docx", "ExtractTextUnderHeading", "Experience", "CheckExperience")
    await run_document_check(f"{data_path}/correct/correct.docx", "ExtractTextUnderHeading", "Team", "CheckQualifications")
    await run_document_check(f"{data_path}/correct/correct.docx", "ExtractTextUnderHeading", "Implementation", "CheckImplementationDescription")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())