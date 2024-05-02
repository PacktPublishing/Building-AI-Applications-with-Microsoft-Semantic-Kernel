import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding, OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.functions import KernelArguments, KernelFunction
from semantic_kernel.prompt_template import PromptTemplateConfig
from semantic_kernel.utils.settings import openai_settings_from_dot_env


async def add_to_memory(memory: SemanticTextMemory, id: str, text: str):
    await memory.save_information(collection="generic", id=id, text=text)

def create_kernel() -> tuple[sk.Kernel, OpenAITextEmbedding]:
    api_key, org_id =  openai_settings_from_dot_env()
    kernel = sk.Kernel()
    gpt = OpenAIChatCompletion(ai_model_id="gpt-4-turbo-preview", api_key=api_key, org_id=org_id, service_id="gpt4")
    emb = OpenAITextEmbedding(ai_model_id="text-embedding-ada-002", api_key=api_key, org_id=org_id, service_id="emb")
    kernel.add_service(emb)
    kernel.add_service(gpt)
    return kernel, emb

async def tour(kernel: sk.Kernel) -> KernelFunction:
    prompt = """
    Information about me, from previous conversations:
    - {{$city}} {{recall $city}}
    - {{$activity}} {{recall $activity}}
    """.strip()

    execution_settings = kernel.get_service("gpt4").instantiate_prompt_execution_settings(service_id="gpt4")
    execution_settings.max_tokens = 4000
    execution_settings.temperature = 0.8

    prompt_template_config = PromptTemplateConfig(template=prompt, execution_settings=execution_settings)    
    chat_func = kernel.add_function(
        function_name="chat_with_memory",
        plugin_name="TextMemoryPlugin",
        prompt_template_config=prompt_template_config,
    )

    return chat_func


async def main():
    kernel, emb = create_kernel()
    memory = SemanticTextMemory(storage=VolatileMemoryStore(), embeddings_generator=emb)
    kernel.add_plugin(TextMemoryPlugin(memory), "TextMemoryPlugin")

    await add_to_memory(memory, id="1", text="My favorite city is Paris")   
    await add_to_memory(memory, id="2", text="My favorite activity is visiting museums")

    f = await tour(kernel)

    args = KernelArguments()
    args["city"] = "My favorite city is Paris"
    args["activity"] = "My favorite activity is visiting museums" 
    answer = await kernel.invoke(f, arguments=args)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
