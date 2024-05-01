import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding, OpenAIChatCompletion
from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.functions import KernelArguments

async def add_to_memory(memory: SemanticTextMemory, id: str, text: str):
    await memory.save_information(collection="generic", id=id, text=text)

def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    emb = OpenAITextEmbedding(ai_model_id="text-embedding-3-small", api_key=api_key, org_id="", service_id="emb3")
    gpt = OpenAIChatCompletion(ai_model_id="gpt-4-turbo-preview", api_key=api_key, org_id="", service_id="gpt4")
    kernel.add_service(gpt)
    kernel.add_service(emb)

    memory = SemanticTextMemory(storage=VolatileMemoryStore(), embeddings_generator=emb)
    kernel.add_plugin(TextMemoryPlugin(memory), "TextMemoryPlugin")
    return kernel, memory

async def tour(kernel: sk.Kernel):
    prompt = """  
    Information about me, from previous conversations:
    - {{$city}} {{recall $city}}
    - {{$activity}} {{recall $activity}}

    Generate a personalized tour of activities for me to do when I have a free day in my favorite city. I just want to do my favorite activity.
    """

    execution_settings = kernel.get_service("gpt4").instantiate_prompt_execution_settings(service_id="gpt4")
    execution_settings.max_tokens = 4000
    execution_settings.temperature = 0.8

    context = KernelArguments()

    f = kernel.add_function ("chat", function_name="chat", prompt=prompt, prompt_execution_settings=execution_settings)
    context["city"] = "What's my favorite city?"
    context["activity"] = "What is my favorite activity?"

    return f, context


async def main():
    load_dotenv()
    kernel, memory = create_kernel()

    await add_to_memory(memory, "1", "My favorite city is Paris")
    await add_to_memory(memory, "2", "My favorite activitity is visiting museums")

    f, context = await tour(kernel)

    answer = await kernel.invoke(f, arguments=context)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
