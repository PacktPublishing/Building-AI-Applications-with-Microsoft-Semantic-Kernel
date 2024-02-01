import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.core_skills import ConversationSummarySkill
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    gpt = OpenAIChatCompletion(ai_model_id="gpt-4-turbo-preview", api_key=api_key, org_id="")
    kernel.add_chat_service("gpt4", gpt)
    kernel.import_skill(ConversationSummarySkill(kernel=kernel), skill_name="ConversationSummaryPlugin")
    return kernel

async def chat(kernel, context) -> bool:   
    user_input = input("User:> ")
    context["userInput"] = user_input
    if user_input == "exit":
        print("\n\nExiting chat...")
        return False

    prompt = """  
    Chat history:
    {{$history}}

    User: {{$userInput}}
    Assistant: 
    """

    f = kernel.create_semantic_function(prompt, max_tokens=4000, temperature=0.8)
    answer = await kernel.run_async(f, input_vars=context.variables)
    context["history"] += f"\nUser:> {user_input}\nAssistant:> {answer}\n"
    print(f"Assistant:> {answer}")
    return True

async def chat_with_summarized_memory(kernel, context) -> bool:   
    user_input = input("User:> ")
    context["userInput"] = user_input
    if user_input == "exit":
        print("\n\nExiting chat...")
        return False

    prompt = """  
    Chat history:
    {{ConversationSummaryPlugin.SummarizeConversation $history}}

    User: {{$userInput}}
    Assistant: 
    """
    f = kernel.create_semantic_function(prompt, max_tokens=4000, temperature=0.8)

    answer = await kernel.run_async(f, input_vars=context.variables)
    context["history"] += f"\nUser:> {user_input}\nAssistant:> {answer}\n"
    print(f"Assistant:> {answer}")
    return True


async def main():
    load_dotenv()
    kernel = create_kernel()

    context = kernel.create_new_context()
    context["history"] = ""

    print("Begin chatting (type 'exit' to exit):\n")
    chatting = True
    while chatting:
        chatting = await chat_with_summarized_memory(kernel, context)
        chatting = await chat(kernel, context)


if __name__ == "__main__":
    asyncio.run(main())
