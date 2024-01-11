from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.planning.stepwise_planner import StepwisePlanner
import semantic_kernel as sk
from dotenv import load_dotenv

def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id)
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)
    kernel.add_chat_service("gpt4", gpt4)
    kernel.add_chat_service("gpt35", gpt35)


    planner = StepwisePlanner(kernel)
    kernel.import_semantic_skill_from_directory("../plugins", "jokes")
    plan = planner.create_plan ("Create four knock-knock jokes: two about dogs, one about cats and one about ducks")

    result = plan.invoke()
    print(result)


if __name__ == "__main__":
    load_dotenv()
    main()