import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding, OpenAIChatCompletion
from LinkedInPlugin import LinkedInPlugin
from BingSearch import BingSearch

async def add_to_memory(kernel: sk.Kernel, id: str, text: str):
    await kernel.memory.save_information_async(collection="default", id=id, text=text)

def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    gpt = OpenAIChatCompletion(ai_model_id="gpt-4-turbo-preview", api_key=api_key, org_id="")
    kernel.add_chat_service("gpt4", gpt)
    return kernel

async def main():
    load_dotenv()
    # kernel = create_kernel()
    bing = BingSearch()
    news = bing.TopTechNewsToday()

    prompt = f"""
    I'm going to provide you with the top 5 technology news articles today.
    1. {news[0]["name"]} - {news[0]["description"]}
    2. {news[1]["name"]} - {news[1]["description"]}
    3. {news[2]["name"]} - {news[2]["description"]}
    4. {news[3]["name"]} - {news[3]["description"]}
    5. {news[4]["name"]} - {news[4]["description"]}

    Choose two articles that you think are the most interesting and write a LinkedIn post about them. 
    The text you generate should be in plain text format and should be ready to be posted on LinkedIn.
    """

    kernel = create_kernel()
    f = kernel.create_semantic_function(prompt, "GeneratePost", max_tokens=3000, temperature=0.7)
    response = await f()   
    post_text = "I have created the post below using the Microsoft Semantic Kernel.\n\n" + str(response) + "\n\nI'm sorry for putting automatically generated content in your feed. I don't like it either, and I'm not going to be doing it often. "
    post_text += "This is just me trying to understand better the capabilities of the Semantic Kernel, by combining a few plugins I just wrote: a plugin that performs a Bing search, a plugin that generates text using the GPT-4 model, and a plugin that posts to LinkedIn. "
    linkedin_plugin = kernel.import_plugin(LinkedInPlugin(), "LinkedInPlugin")
    result = await linkedin_plugin["CreateTextPost"](post_text)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
