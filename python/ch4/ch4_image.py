import asyncio
import semantic_kernel as sk
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from OpenAiPlugins import Dalle3

async def pipeline(kernel, function_list, input):
    for function in function_list:
        args = KernelArguments(input=input)
        input = await kernel.invoke(function, args)
    return input

async def main():
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, "gpt35")
    kernel.add_service(gpt35)

    generate_image_plugin = kernel.add_plugin(Dalle3(), "Dalle3")
    animal_guesser = kernel.add_plugin(None, plugin_name="AnimalGuesser", parent_directory="../../plugins")

    clues = """
    I am thinking of an animal.
    It is a mammal.
    It is a pet.
    It is a carnivore.
    It purrs."""
    
    function_list = [
        animal_guesser['GuessAnimal'],
        generate_image_plugin['ImageFromPrompt']
    ]

    animal_pic_url = await pipeline(kernel, function_list, clues)
    print(animal_pic_url)


if __name__ == "__main__":
    asyncio.run(main())