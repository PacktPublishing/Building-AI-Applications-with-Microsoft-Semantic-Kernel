import asyncio
import semantic_kernel as sk
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from OpenAiPlugins import Dalle3

async def main():
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, "gpt35")
    kernel.add_service(gpt35)

    dalle3 = kernel.add_plugin(Dalle3(), "Dalle3")
    animal_str = "A painting of a cat sitting on a sofa in the impressionist style"

    animal_pic_url = await kernel.invoke(dalle3['ImageFromPrompt'], KernelArguments(input = animal_str))
    print(animal_pic_url)

if __name__ == "__main__":
    asyncio.run(main())