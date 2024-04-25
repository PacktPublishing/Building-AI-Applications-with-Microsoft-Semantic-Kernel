from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
from HomeAutomation import HomeAutomation
from dotenv import load_dotenv
import asyncio

async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()
    gpt4 = OpenAIChatCompletion("gpt-4-turbo-preview", api_key, org_id)
    kernel.add_service(gpt4)
    kernel.import_plugin_from_object(HomeAutomation(), "HomeAutomation")
    
    r1 = await kernel.invoke(kernel.plugins["HomeAutomation"]["OperateWindow"], location="living room", action="open")
    r2 = await kernel.invoke(kernel.plugins["HomeAutomation"]["OperateLight"], location="kitchen", action="on")
    r3 = await kernel.invoke(kernel.plugins["HomeAutomation"]["OperateGarageDoor"], action="close")
    print(r1)
    print(r2)
    print(r3)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())