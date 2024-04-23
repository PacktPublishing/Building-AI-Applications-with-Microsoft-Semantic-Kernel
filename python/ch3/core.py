import asyncio
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.utils.settings import openai_settings_from_dot_env
import semantic_kernel as sk
from semantic_kernel.core_plugins.time_plugin import TimePlugin

async def main():

    kernel = sk.Kernel()
    api_key, org_id = openai_settings_from_dot_env()
    gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id, "gpt35")

    kernel.add_service(gpt35)    
    kernel.add_plugin(TimePlugin(), "time")

    prompt  = """
    Today is: {{time.date}}
    Current time is: {{time.time}}

    Answer to the following questions using JSON syntax, including the data used.
    Is it morning, afternoon, evening, or night (morning/afternoon/evening/night)?
    Is it weekend time (weekend/not weekend)?
    """
    prompt_function = kernel.add_function(function_name="ex01", plugin_name="sample", prompt=prompt)
    response = await kernel.invoke(prompt_function, request=prompt)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())