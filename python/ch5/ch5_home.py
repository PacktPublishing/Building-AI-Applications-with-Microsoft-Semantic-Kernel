import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.planners import FunctionCallingStepwisePlanner, FunctionCallingStepwisePlannerOptions
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from HomeAutomation import HomeAutomation
import semantic_kernel as sk

async def fulfill_request(kernel: sk.Kernel, planner: FunctionCallingStepwisePlanner, request):
    print("Fulfilling request: " + request)	   
    result = await planner.invoke(kernel, request)
    print(result.final_answer)
    print("Request completed.\n\n")


async def main():
    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id, service_id = "gpt4")
    kernel.add_service(gpt4)
    planner_options = FunctionCallingStepwisePlannerOptions(
        max_tokens=4000,
    )
    planner = FunctionCallingStepwisePlanner(service_id="gpt4", options=planner_options)
    kernel.add_plugin(HomeAutomation(), "HomeAutomation")
    kernel.add_plugin(None, plugin_name="MovieRecommender", parent_directory="../../plugins")
    
    await fulfill_request(kernel, planner, "Turn on the lights in the kitchen")
    await fulfill_request(kernel, planner, "Open the windows of the bedroom, turn the lights off and put on Shawshank Redemption on the TV.")   
    await fulfill_request(kernel, planner, "Close the garage door and turn off the lights in all rooms.")
    await fulfill_request(kernel, planner, "Turn off the lights in all rooms and play a movie in which Tom Cruise is a lawyer in the living room.")

if __name__ == "__main__":
    asyncio.run(main())