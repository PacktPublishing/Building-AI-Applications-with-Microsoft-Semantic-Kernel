import asyncio
import semantic_kernel as sk
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from Helpers import Helpers
from CheckSpreadsheet import CheckSpreadsheet
from ParseWordDocument import ParseWordDocument
import os

async def pipeline(kernel, function_list, input):
    for function in function_list:
        args = KernelArguments(input=input)
        input = await kernel.invoke(function, args)
    return input

async def main():
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id, "gpt4")
    kernel.add_service(gpt4)

    parse_word_document = kernel.add_plugin(ParseWordDocument(), "ParseWordDocument")
    check_spreadsheet = kernel.add_plugin(CheckSpreadsheet(), "CheckSpreadsheet")
    helpers = kernel.add_plugin(Helpers(), "Helpers")
    interpret_document = kernel.add_plugin(None, "ProposalCheckerV2", "../../plugins")

    data_path = "../../data/proposals/"

    for folder in os.listdir(data_path):
        if not os.path.isdir(os.path.join(data_path, folder)):
            continue
        print(f"\n\nProcessing folder: {folder}") 
        function_list = [
            helpers['ProcessProposalFolder'],
            check_spreadsheet['CheckTabs'],
            check_spreadsheet['CheckCells'],
            check_spreadsheet['CheckValues'],
            parse_word_document['ExtractTeam'],
            interpret_document['CheckTeamV2'],
            parse_word_document['ExtractExperience'],
            interpret_document['CheckPreviousProjectV2'],
            parse_word_document['ExtractImplementation'],
            interpret_document['CheckDatesV2']
        ]
        process_result = await pipeline(kernel, function_list, os.path.join(data_path, folder))
        
        result = (str(process_result))
        if result.startswith("Error"):
            print(result)
            continue
        else:
            print("Success")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())