using System.ComponentModel;
using Microsoft.SemanticKernel;
public class HomeAutomation
{
    [KernelFunction, Description("Turns the lights of the living room, kitchen, bedroom or garage on or off.")]
    public string OperateLight(
        [Description("Whether to turn the lights on or off. Must be either 'on' or 'off'")] string action, 
        [Description("The location where the lights must be turned on or off. Must be 'living room', 'bedroom', 'kitchen' or 'garage'")] string location)
    {
        string[] validLocations = {"kitchen", "living room", "bedroom", "garage" };
        if (validLocations.Contains(location))
        {
            string exAction = $"Changed status of the {location} lights to {action}.";
            Console.WriteLine(exAction);
            return exAction;
        }
        else
        {
            string error = $"Invalid location {location} specified.";
            return error;
        }
    }

    [KernelFunction, Description("Opens or closes the windows of the living room or bedroom.")]
    public string OperateWindow(
        [Description("Whether to open or close the windows. Must be either 'open' or 'close'")] string action, 
        [Description("The location where the windows are to be opened or closed. Must be either 'living room' or 'bedroom'")] string location)
    {
        string[] validLocations = {"living room", "bedroom"};
        if (validLocations.Contains(location))
        {
            string exAction = $"Changed status of the {location} windows to {action}.";
            Console.WriteLine(exAction);
            return exAction;
        }
        else
        {
            string error = $"Invalid location {location} specified.";
            return error;
        }
    }

    [KernelFunction, Description("Puts a movie on the TV in the living room or bedroom.")]
    public string OperateTV(
        [Description("The movie to play on the TV.")] string movie, 
        [Description("The location where the movie should be played on. Must be 'living room' or 'bedroom'")] string location)
    {
        string[] validLocations = {"living room", "bedroom"};
        if (validLocations.Contains(location))
        {
            string exAction = $"Playing {movie} on the TV in the {location}.";
            Console.WriteLine(exAction);
            return exAction;
        }
        else
        {
            string error = $"Invalid location {location} specified.";
            return error;
        }
    }

    [KernelFunction, Description("Opens or closes the garage door.")]
    public string OperateGarageDoor(
        [Description("The action to perform on the garage door. Must be either 'open' or 'close'")] string action)
    {
        string exAction = $"Changed status of the garage door to {action}.";
        Console.WriteLine(exAction);
        return exAction;
    }            
}
