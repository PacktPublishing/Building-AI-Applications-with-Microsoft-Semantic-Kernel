using System.ComponentModel;
using System.Globalization;
using Microsoft.SemanticKernel.SkillDefinition;

namespace Plugins;

public class ShowManager
{
    [SKFunction, Description("Returns a random string from a list of strings")]
    public string RandomTheme()
    {
        var list = new List<string> { "boo", "dishes", "art", "needle", "tank", "police"};
        return list[new Random().Next(0, list.Count)];
    }
}