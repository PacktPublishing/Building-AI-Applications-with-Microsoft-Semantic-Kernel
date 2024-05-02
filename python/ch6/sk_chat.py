import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelFunction
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable
from semantic_kernel.core_plugins import ConversationSummaryPlugin
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.utils.settings import openai_settings_from_dot_env

async def main():
    kernel = create_kernel()
    history = ChatHistory()

    chat_function = await create_chat_function(kernel)

    while True:
        try:
            request = input("User:> ")
        except KeyboardInterrupt:
            print("\n\nExiting chat...")
            return False
        except EOFError:
            print("\n\nExiting chat...")
            return False

        if request == "exit":
            print("\n\nExiting chat...")
            return False

        result = await kernel.invoke(
            chat_function,
            request=request,
            history=history,
        )

        # Add the request to the history
        history.add_user_message(request)
        history.add_assistant_message(str(result))

        print(f"Assistant:> {result}")

def create_kernel() -> sk.Kernel:
    api_key, org_id =  openai_settings_from_dot_env()
    kernel = sk.Kernel()
    gpt = OpenAIChatCompletion(ai_model_id="gpt-4-turbo-preview", api_key=api_key, org_id=org_id, service_id="gpt4")
    kernel.add_service(gpt)

    # The following execution settings are used for the ConversationSummaryPlugin
    execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="gpt4", max_tokens=ConversationSummaryPlugin._max_tokens, temperature=0.1, top_p=0.5)
    
    prompt_template_config = PromptTemplateConfig(
        template=ConversationSummaryPlugin._summarize_conversation_prompt_template,
        description="Given a section of a conversation transcript, summarize it",
        execution_settings=execution_settings,
    )    

    # Import the ConversationSummaryPlugin
    kernel.add_plugin(
        ConversationSummaryPlugin(kernel=kernel, prompt_template_config=prompt_template_config),
        plugin_name="ConversationSummaryPlugin",
    )

    return kernel


async def create_chat_function(kernel: sk.Kernel) -> KernelFunction:   
    # Create the prompt with the ConversationSummaryPlugin
    prompt = """{{ConversationSummaryPlugin.SummarizeConversation $history}}
    User: {{$request}}
    Assistant:  """

    # These execution settings are tied to the chat function, created below.
    execution_settings = kernel.get_service("gpt4").instantiate_prompt_execution_settings(service_id="gpt4")
    chat_prompt_template_config = PromptTemplateConfig(
        template=prompt,
        description="Chat with the assistant",
        execution_settings=execution_settings,
        input_variables=[
            InputVariable(name="request", description="The user input", is_required=True),
            InputVariable(name="history", description="The history of the conversation", is_required=True),
        ],
    )

    # Create the function
    chat_function = kernel.add_function(
        prompt=prompt,
        plugin_name="Summarize_Conversation",
        function_name="Chat",
        description="Chat with the assistant",
        prompt_template_config=chat_prompt_template_config,)
    
    return chat_function


if __name__ == "__main__":
    asyncio.run(main())
