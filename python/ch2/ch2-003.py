import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.utils.settings import openai_settings_from_dot_env
import semantic_kernel as sk
from semantic_kernel.functions.kernel_arguments import KernelArguments

async def main():
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, "gpt35")

    kernel.add_service(gpt35)
    
    pe_plugin = kernel.add_plugin(None, parent_directory="../../plugins", plugin_name="prompt_engineering")
    response = await kernel.invoke(pe_plugin["attractions_multiple_variables"], KernelArguments(
        city = "New York City",
        n_days = "3",
        likes = "restaurants, Ghostbusters, Friends tv show",
        dislikes = "museums, parks",
        n_attractions = "5"
    ))
    print(response)


if __name__ == "__main__":
    asyncio.run(main())