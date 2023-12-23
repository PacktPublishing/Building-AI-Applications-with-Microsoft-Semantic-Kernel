import asyncio
import semantic_kernel as sk
from OpenAiPlugins import Dalle3

async def main():
    kernel = sk.Kernel()
    animal_str = "A painting of a cat sitting in a sofa in the impressionist style"
    dalle3 = kernel.import_skill(Dalle3())

    animal_pic_url = await kernel.run_async(
        dalle3['ImageFromPrompt'],
        input_str=animal_str
    )

    print(animal_pic_url)

if __name__ == "__main__":
    asyncio.run(main())