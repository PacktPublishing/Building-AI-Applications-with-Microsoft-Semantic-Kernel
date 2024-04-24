from dotenv import load_dotenv
from openai import OpenAI
import os
from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class Dalle3:
    @kernel_function(
        description="Generates an with DALL-E 3 model based on a prompt",
        name="ImageFromPrompt",
    )
    def ImageFromPrompt(self, input: Annotated[str, "The prompt used to generate the image"] ) -> str:
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