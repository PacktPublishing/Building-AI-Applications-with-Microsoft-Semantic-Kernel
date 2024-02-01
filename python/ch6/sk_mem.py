import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding, OpenAIChatCompletion

async def add_to_memory(kernel: sk.Kernel, id: str, text: str):
    await kernel.memory.save_information_async(collection="default", id=id, text=text)

def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    emb = OpenAITextEmbedding(ai_model_id="text-embedding-3-small", api_key=api_key, org_id="")
    gpt = OpenAIChatCompletion(ai_model_id="gpt-4-turbo-preview", api_key=api_key, org_id="")
    kernel.add_chat_service("gpt4", gpt)
    kernel.add_text_embedding_generation_service("emb3", emb)
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    kernel.import_skill(sk.core_skills.TextMemorySkill())
    return kernel

async def tour(kernel: sk.Kernel):
    prompt = """  
    Information about me, from previous conversations:
    - {{$city}} {{recall $city}}
    - {{$activity}} {{recall $activity}}

    Generate a personalized tour of activities for me to do when I have a free day in my favorite city. I just want to do my favorite activity.
    """

    f = kernel.create_semantic_function(prompt, max_tokens=2000, temperature=0.8)
    context = kernel.create_new_context()
    context["city"] = "What's my favorite city?"
    context["activity"] = "What is my favorite activity?"
    context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = "default"
    context[sk.core_skills.TextMemorySkill.RELEVANCE_PARAM] = "0.6"

    return f, context


async def main():
    load_dotenv()
    kernel = create_kernel()

    await add_to_memory(kernel, "1", "My favorite city is Paris")
    await add_to_memory(kernel, "2", "My favorite activitity is visiting museums")

    f, context = await tour(kernel)

    answer = await kernel.run_async(f, input_vars=context.variables)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
