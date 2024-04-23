import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.planners import FunctionCallingStepwisePlanner, FunctionCallingStepwisePlannerOptions
from semantic_kernel.utils.settings import openai_settings_from_dot_env
import semantic_kernel as sk

async def main():
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()

    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, service_id = "gpt35")
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id, service_id = "gpt4")

    kernel.add_service(gpt35)
    kernel.add_service(gpt4)
    kernel.add_plugin(None, plugin_name="jokes", parent_directory="../../plugins/")

    planner_options = FunctionCallingStepwisePlannerOptions(
        max_tokens=4000,
    )
    planner = FunctionCallingStepwisePlanner(service_id="gpt4", options=planner_options)

    prompt = "Create four knock-knock jokes: two about dogs, one about cats and one about ducks"
    result = await planner.invoke(kernel, prompt)

    print(result.final_answer)


if __name__ == "__main__":
    asyncio.run(main())