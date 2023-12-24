import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from CheckSpreadsheet import CheckSpreadsheet
from ParseWordDocument import ParseWordDocument
from Helpers import Helpers
import os

async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id)
    kernel.add_chat_service("gpt4", gpt4)

    parse_word_document = kernel.import_skill(ParseWordDocument())
    check_spreadsheet = kernel.import_skill(CheckSpreadsheet())
    helpers = kernel.import_skill(Helpers())
    interpret_document = kernel.import_semantic_skill_from_directory("../../plugins", "ProposalCheckerV2")

    data_path = "../../data/proposals/"

    for folder in os.listdir(data_path):
        if not os.path.isdir(os.path.join(data_path, folder)):
            continue
        print(f"\n\nProcessing folder: {folder}") 
        process_result = await kernel.run_async(
            helpers['ProcessProposalFolder'],
            check_spreadsheet['CheckTabs'],
            check_spreadsheet['CheckCells'],
            check_spreadsheet['CheckValues'],
            parse_word_document['ExtractTeam'],
            interpret_document['CheckTeamV2'],
            parse_word_document['ExtractExperience'],
            interpret_document['CheckPreviousProjectV2'],
            parse_word_document['ExtractImplementation'],
            interpret_document['CheckDatesV2'],
            input_str=os.path.join(data_path, folder)
        ) 

        result = (str(process_result))
        if result.startswith("Error"):
            print(result)
            continue
        else:
            print("Success")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())