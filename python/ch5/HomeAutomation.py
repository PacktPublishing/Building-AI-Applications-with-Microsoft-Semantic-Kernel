from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext

class HomeAutomation:
    def __init__(self):
        pass

    @sk_function(
        description="Opens or closes the windows of the living room or bedroom.",
        name="OperateWindow",
    )
    @sk_function_context_parameter(
        name="action",
        type="string",	
        description="Whether to open or close the windows. Must be either 'open' or 'close'",
        required=True,
    )
    @sk_function_context_parameter(
        name="location",
        type="string",	
        description="The location where the windows are to be opened or closed. Must be either 'living room' or 'bedroom'",
        required=True,
    )        
    def OperateWindow(self, context: SKContext) -> str:
        if context['location'] in ["living room", "bedroom"]:
            action = f"Changed status of the {context['location']} windows to {context['action']}."
            print(action)
            return action
        else:
            error = f"Invalid location {context['location']} specified."
            return error

    @sk_function(
        description="Turns the lights of the living room, kitchen, bedroom or garage on or off.",
        name="OperateLight",
    )
    @sk_function_context_parameter(
        name="action",
        type="string",	
        description="Whether to turn the lights on or off. Must be either 'on' or 'off'",
        required=True,
    )
    @sk_function_context_parameter(
        name="location",
        type="string",	
        description="The location where the lights must be turned on or off. Must be 'living room', 'bedroom', 'kitchen' or 'garage'",
        required=True,
    )        
    def OperateLight(self, context: SKContext) -> str:
        if context['location'] in ["kitchen", "living room", "bedroom", "garage"]:
            action = f"Changed status of the {context['location']} lights to {context['action']}."
            print(action)
            return action
        else:
            error = f"Invalid location {context['location']} specified."
            return error

    @sk_function(
        description="Puts a movie on the TV in the living room or bedroom.",
        name="OperateTV",
    )
    @sk_function_context_parameter(
        name="movie",
        type="string",
        description="The movie to play on the TV.",
        required=True,
    )
    @sk_function_context_parameter(
        name="location",
        type="string",
        description="The location where the movie should be played on. Must be 'living room' or 'bedroom'",
        required=True,
    )  
    def OperateTV(self, context: SKContext) -> str:
        if context['location'] in ["living room", "bedroom"]:
            action = f"Playing {context['movie']} on the TV in the {context['location']}."
            print(action)
            return action
        else:
            error = f"Invalid location {context['location']} specified."
            return error

    @sk_function(
        description="Opens or closes the garage door.",
        name="OperateGarageDoor",
        input_description="The action to perform on the garage door. Must be either 'open' or 'close'",
    )
    def OperateGarageDoor(self, action: str) -> str:
        action = f"Changed the status of the garage door to {context['action']}."
        print(action)
        return action
