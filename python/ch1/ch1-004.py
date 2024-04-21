import random
import asyncio
import semantic_kernel as sk
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.kernel_arguments import KernelArguments

async def main():
    kernel = sk.Kernel()

    api_key, org_id = openai_settings_from_dot_env()

    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, service_id = "gpt35")
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id, service_id = "gpt4")

    kernel.add_service(gpt35)
    kernel.add_service(gpt4)

    theme_plugin = kernel.add_plugin(ShowManager(), "ShowManager")
    theme = await kernel.invoke(theme_plugin["random_theme"])

    jokes_plugin = kernel.add_plugin(None, parent_directory="../../plugins", plugin_name="jokes")

    knock_joke = await kernel.invoke(jokes_plugin["knock_knock_joke"], KernelArguments(input=theme))
    print(knock_joke)

    explanation = await kernel.invoke(jokes_plugin["explain_joke"], KernelArguments(input=knock_joke))
    print(explanation)


class ShowManager:
    @kernel_function(
        description="Randomly choose among a theme for a joke",
        name="random_theme"
    )
    def random_theme(self) -> str:
        themes = ["Boo", "Dishes", "Art", 
                "Needle", "Tank", "Police"]
        # choose a random element of the list
        theme = random.choice(themes)
        return theme

if __name__ == "__main__":
    asyncio.run(main())
