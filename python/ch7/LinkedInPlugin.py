from semantic_kernel.plugin_definition import kernel_function, kernel_function_context_parameter
from semantic_kernel.orchestration.kernel_context import KernelContext
from LinkedInPoster import LinkedInPoster

class LinkedInPlugin:
    def __init__(self):
        pass

    @kernel_function(
        description="Create a text post in LinkedIn",
        name="CreateTextPost",
        input_description="The contents of the text post",
    )
    def CreateTextPost(self, content: str) -> str:
        linkedin_poster = LinkedInPoster()
        return linkedin_poster.CreateTextPost(content)

    @kernel_function(
        description="Creates a media post",
        name="CreateMediaPost",
    )
    @kernel_function_context_parameter(
        name="content",
        type="string",	
        description="The content of the post",
        required=True,
    )
    @kernel_function_context_parameter(
        name="imnage_url",
        type="string",	
        description="The URL of the image to attach to the post",
        required=True,
    )        
    def CreateMediaPost(self, context: KernelContext) -> str:
        action = f"Created a media post with content {context['content']} and image URL {context['image_url']}."
        print(action)
        return action
