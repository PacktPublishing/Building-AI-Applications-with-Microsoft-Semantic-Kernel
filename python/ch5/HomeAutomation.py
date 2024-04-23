from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class HomeAutomation:
    def __init__(self):
        pass

    @kernel_function(
        description="Opens or closes the windows of the living room or bedroom.",
        name="OperateWindow",
    )
    def OperateWindow(self, 
            location: Annotated[str, "The location where the windows are to be opened or closed. Must be either 'living room' or 'bedroom'"],
            action: Annotated[str, "Whether to open or close the windows. Must be either 'open' or 'close'"]) \
                -> Annotated[str, "The action that was performed on the windows."]:
        if location in ["living room", "bedroom"]:
            action = f"Changed status of the {location} windows to {action}."
            print(action)
            return action
        else:
            error = f"Invalid location {location} specified."
            return error

    @kernel_function(
        description="Turns the lights of the living room, kitchen, bedroom or garage on or off.",
        name="OperateLight",
    )
    def OperateLight(self, 
            location: Annotated[str, "The location where the lights are to be turned on or off. Must be either 'living room', 'kitchen', 'bedroom' or 'garage'"],
            action: Annotated[str, "Whether to turn the lights on or off. Must be either 'on' or 'off'"])\
                -> Annotated[str, "The action that was performed on the lights."]:
        if location in ["kitchen", "living room", "bedroom", "garage"]:
            action = f"Changed status of the {location} lights to {action}."
            print(action)
            return action
        else:
            error = f"Invalid location {location} specified."
            return error

    @kernel_function(
        description="Puts a movie on the TV in the living room or bedroom.",
        name="OperateTV",
    )
    def OperateTV(self, 
            movie: Annotated[str, "The movie to play on the TV."],
            location: Annotated[str, "The location where the movie should be played on. Must be 'living room' or 'bedroom'"]
            )\
                -> Annotated[str, "The action that was performed on the TV."]:
        if location in ["living room", "bedroom"]:
            action = f"Playing {movie} on the TV in the {location}."
            print(action)
            return action
        else:
            error = f"Invalid location {location} specified."
            return error

    @kernel_function(
        description="Opens or closes the garage door.",
        name="OperateGarageDoor"
    )
    def OperateGarageDoor(self, 
            action: Annotated[str, "The action to perform on the garage door. Must be either 'open' or 'close'"])\
                  -> Annotated[str, "The action that was performed on the garage door."]:
        action = f"Changed the status of the garage door to {action}."
        print(action)
        return action
