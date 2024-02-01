from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.planning.stepwise_planner import StepwisePlanner
import semantic_kernel as sk
from HomeAutomation import HomeAutomation
from dotenv import load_dotenv
import asyncio

async def fulfill_request(planner: StepwisePlanner, request):
    print("Fulfilling request: " + request)	   
    variables = sk.ContextVariables()
    plan = planner.create_plan(request)
    result = await plan.invoke_async(variables)
    print(result)
    print("Request completed.\n\n")


async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id)
    kernel.add_chat_service("gpt4", gpt4)
    planner = StepwisePlanner(kernel)
    kernel.import_skill(HomeAutomation())
    kernel.import_semantic_skill_from_directory("../plugins/MovieRecommender", "RecommendMovie")
    
    await fulfill_request(planner, "Turn on the lights in the kitchen")
    await fulfill_request(planner, "Open the windows of the bedroom, turn the lights off and put on Shawshank Redemption on the TV.")   
    await fulfill_request(planner, "Close the garage door and turn off the lights in all rooms.")
    await fulfill_request(planner, "Turn off the lights in all rooms and play a movie in which Michael Keaton is a superhero in the bedroom.")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())asdasd