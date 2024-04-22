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
    
    problem = """When I was 6 my sister was half my age. Now I'm 70. How old is my sister?"""

    pe_plugin = kernel.add_plugin(None, parent_directory="../../plugins", plugin_name="prompt_engineering")
   
    responses = []

    for i in range(7):
        solve_steps = await kernel.invoke(pe_plugin["solve_math_problem_v2"], KernelArguments(problem = problem))
        response = await kernel.invoke(pe_plugin["chain_of_thought_v2"], KernelArguments(problem = problem, input = solve_steps))
        responses.append(int(str(response)))

    print("Responses:")
    print(responses)

    final_answer = max(set(responses), key = responses.count)
    print(f"Final answer: {final_answer}")

if __name__ == "__main__":
    asyncio.run(main())