import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from CheckSpreadsheet import CheckSpreadsheet
from ParseWordDocument import ParseWordDocument
from semantic_kernel.functions.kernel_arguments import KernelArguments

async def run_spreadsheet_check(path, function):
    kernel = sk.Kernel()
    
    check_spreadsheet = kernel.add_plugin(CheckSpreadsheet(), "CheckSpreadsheet")

    result = await kernel.invoke(
        check_spreadsheet[function], KernelArguments(path = path)
    )
    print(result)


async def run_document_check(path, function, target_heading, semantic_function):
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, service_id = "gpt35")
    kernel.add_service(gpt35)

    parse_word_document = kernel.add_plugin(ParseWordDocument(), "ParseWordDocument")

    text = await kernel.invoke(
        parse_word_document[function],
        KernelArguments(doc_path = path, target_heading = target_heading)
    )

    check_docs = kernel.add_plugin(None, "ProposalChecker", "../../plugins")
    result = await kernel.invoke(check_docs[semantic_function], KernelArguments(input = text))
    print(f"{target_heading}: {result}")

async def main():
    data_path = "../../data/proposals"
    await run_spreadsheet_check(f"{data_path}/correct/correct.xlsx", "CheckValues")
    await run_spreadsheet_check(f"{data_path}/incorrect01/incorrect_template.xlsx", "CheckTabs")
    await run_spreadsheet_check(f"{data_path}/incorrect02/over_budget.xlsx", "CheckValues")
    await run_spreadsheet_check(f"{data_path}/incorrect03/fast_increase.xlsx", "CheckValues")
    
    # await run_spreadsheet_check(f"{data_path}/correct/correct.xlsx", "CheckCells")
    # await run_spreadsheet_check(f"{data_path}/incorrect04/incorrect_cells.xlsx", "CheckCells")
    # await run_spreadsheet_check(f"{data_path}/incorrect02/over_budget.xlsx", "CheckCells")
    # await run_spreadsheet_check(f"{data_path}/incorrect03/fast_increase.xlsx", "CheckCells")

    # await run_spreadsheet_check(f"{data_path}/correct/correct.xlsx", "CheckValues")
    # await run_spreadsheet_check(f"{data_path}/incorrect02/over_budget.xlsx", "CheckValues")
    # await run_spreadsheet_check(f"{data_path}/incorrect03/fast_increase.xlsx", "CheckValues")

    print("Word document checks:")

    await run_document_check(f"{data_path}/correct/correct.docx", "ExtractTextUnderHeading", "Experience", "CheckExperience")
    await run_document_check(f"{data_path}/correct/correct.docx", "ExtractTextUnderHeading", "Team", "CheckQualifications")
    await run_document_check(f"{data_path}/correct/correct.docx", "ExtractTextUnderHeading", "Implementation", "CheckImplementationDescription")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())