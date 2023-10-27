from semantic_kernel.skill_definition import sk_function
import random
import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from semantic_kernel.planning.basic_planner import BasicPlanner

class ShowManager:
    @sk_function(
        description="Choose a random theme for a joke",
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

    show_manager = ShowManager()
    kernel.import_skill(show_manager, skill_name="show_manager")
    kernel.import_semantic_skill_from_directory("../../plugins", "jokes")

    planner = BasicPlanner()

    ask = f"""Choose a random theme for a joke, generate a knock-knock joke about it and explain it"""
    plan = await planner.create_plan_async(ask, kernel)

    print(plan.generated_plan)

    joke_and_explanation = await planner.execute_plan_async(plan, kernel)
    print(joke_and_explanation)



if __name__ == "__main__":
    asyncio.run(main())