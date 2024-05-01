import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.core_plugins import ConversationSummaryPlugin
from semantic_kernel.functions import KernelArguments

def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    gpt = OpenAIChatCompletion("gpt-4-turbo-preview", api_key, None, "gpt4")
    kernel.add_service(gpt)
    
    kernel.add_plugin(ConversationSummaryPlugin(kernel, None, "history"), "ConversationSummaryPlugin")
    return kernel

async def chat(kernel:sk.Kernel, context: KernelArguments) -> bool:   
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

    execution_settings = kernel.get_service("gpt4").instantiate_prompt_execution_settings(service_id="gpt4")
    execution_settings.max_tokens = 4000
    execution_settings.temperature = 0.8

    f = kernel.add_function ("chat", function_name="chat", prompt=prompt, prompt_execution_settings=execution_settings)
    answer = await kernel.invoke(f, arguments=context)
    context["history"] += f"\nUser:> {user_input}\nAssistant:> {answer}\n"
    print(f"Assistant:> {answer}")
    return True

async def chat_with_summarized_memory(kernel: sk.Kernel, context: KernelArguments) -> bool:   
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

    execution_settings = kernel.get_service("gpt4").instantiate_prompt_execution_settings(service_id="gpt4")
    execution_settings.max_tokens = 4000
    execution_settings.temperature = 0.8
    f = kernel.add_function("chat", function_name="chat", prompt=prompt, prompt_execution_settings=execution_settings)

    answer = await kernel.invoke(f, arguments=context)
    context["history"] += f"\nUser:> {user_input}\nAssistant:> {answer}\n"
    print(f"Assistant:> {answer}")
    return True


async def main():
    load_dotenv()
    kernel = create_kernel()

    context = KernelArguments()
    context["history"] = ""

    print("Begin chatting (type 'exit' to exit):\n")
    chatting = True
    while chatting:
        chatting = await chat_with_summarized_memory(kernel, context)
        chatting = await chat(kernel, context)


if __name__ == "__main__":
    asyncio.run(main())
