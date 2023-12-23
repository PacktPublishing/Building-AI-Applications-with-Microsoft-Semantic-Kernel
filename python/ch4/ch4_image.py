import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from OpenAiPlugins import Dalle3

async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)
    kernel.add_chat_service("gpt35", gpt35)

    generate_image_plugin = kernel.import_skill(Dalle3())
    animal_guesser = kernel.import_semantic_skill_from_directory("../../plugins", "AnimalGuesser")

    clues = """
    I am thinking of an animal.
    It is a mammal.
    It is a pet.
    It is a carnivore.
    It purrs."""
    
    animal_pic_url = await kernel.run_async(
        animal_guesser['GuessAnimal'],
        generate_image_plugin['ImageFromPrompt'],
        input_str=clues
    )

    print(animal_pic_url)


if __name__ == "__main__":
    asyncio.run(main())