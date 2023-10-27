import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk

async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)

    kernel.add_chat_service("gpt35", gpt35)

    prompts = kernel.import_semantic_skill_from_directory("../../plugins", "prompt_engineering")

    problem = """When I was 6 my sister was half my age. Now I'm 70. How old is my sister?"""

    solve = prompts['solve_math_problem']

    input_context = kernel.create_new_context()
    input_context['problem'] = problem

    response = await kernel.run_async(
        solve
        , input_context=input_context
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())