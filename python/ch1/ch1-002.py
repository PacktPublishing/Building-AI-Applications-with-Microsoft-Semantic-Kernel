import semantic_kernel as sk
kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()

from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
gpt35 = OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)
gpt4 = OpenAIChatCompletion("gpt-4", api_key, org_id)

kernel.add_chat_service("gpt35", gpt35)
kernel.add_chat_service("gpt4", gpt4)

prompt = """Finish the following knock-knock joke. 
Knock, knock. Who's there? {{$input}}. {{$input}} who?"""

knock = kernel.create_semantic_function(prompt, temperature=0.8)

response = knock("Boo")
print(response)