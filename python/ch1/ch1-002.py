import asyncio
import semantic_kernel as sk
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

async def main():
    kernel = sk.Kernel()

    api_key, org_id = openai_settings_from_dot_env()

    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, service_id = "gpt35")
    gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id, service_id = "gpt4")

    kernel.add_service(gpt35)
    kernel.add_service(gpt4)

    prompt = """Finish the following knock-knock joke. 
    Knock, knock. Who's there? {{$input}}. {{$input}} who?"""

    prompt_function = kernel.add_function(function_name="ex01", plugin_name="sample", prompt=prompt)


    args = KernelArguments(input="Boo")
    response = await kernel.invoke(prompt_function, request=prompt, arguments=args)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
    

