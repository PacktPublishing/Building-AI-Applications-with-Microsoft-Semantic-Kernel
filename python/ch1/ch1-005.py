from semantic_kernel.skill_definition import sk_function
import random
import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk

class ShowManager:
    @sk_function(
        description="Randomly choose among a theme for a joke",
        name="random_theme"
    )
    def random_theme(self) -> str:
        themes = ["Boo", "Dishes", "Art", 
                "Needle", "Tank", "Police"]
        # choose a random element of the list
        theme = random.choice(themes)
        return theme

async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id)

    kernel.add_chat_service("gpt35", gpt35)
    kernel.add_chat_service("gpt4", gpt4)


    theme_choice = kernel.import_skill(ShowManager())

    jokes_plugin = kernel.import_semantic_skill_from_directory("../../plugins", "jokes")

    context = kernel.create_new_context()

    response = await kernel.run_async(
        theme_choice["random_theme"],
        jokes_plugin["knock_knock_joke"],
        jokes_plugin["explain_joke"],
        input_context=context
    )

    print(response)

if __name__ == "__main__":
    asyncio.run(main())