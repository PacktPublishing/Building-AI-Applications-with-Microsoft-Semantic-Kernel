from dotenv import load_dotenv
from openai import OpenAI
import os
from semantic_kernel.skill_definition import sk_function

class Dalle3:
    @sk_function(
        description="Generates an with DALL-E 3 model based on a prompt",
        name="ImageFromPrompt",
        input_description="The prompt used to generate the image",
    )
    def ImageFromPrompt(self, input: str) -> str:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.images.generate(
            model="dall-e-3",
            prompt=input,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url