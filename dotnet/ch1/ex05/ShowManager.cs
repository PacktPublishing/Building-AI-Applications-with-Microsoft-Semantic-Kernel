using System.ComponentModel;
using Microsoft.SemanticKernel;

namespace Plugins;

public class ShowManager
{
    [KernelFunction, Description("Take the square root of a number")]
    public string RandomTheme()
    {
        var list = new List<string> { "boo", "dishes", "art", "needle", "tank", "police"};
        return list[new Random().Next(0, list.Count)];
    }
}