import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from CheckSpreadsheet import CheckSpreadsheet

async def main():
    kernel = sk.Kernel()
    check_spreadsheet = kernel.import_skill(CheckSpreadsheet())

    data_path = "../../data/proposals/"
    result1 = await kernel.run_async(
        check_spreadsheet["CheckTabs"],
        input_str=f"{data_path}/correct/correct.xlsx",
    )
    print(result1)

    result2 = await kernel.run_async(
        check_spreadsheet["CheckTabs"],
        input_str=f"{data_path}/incorrect1/incorrect_template.xlsx",
    )

    print(result2)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())