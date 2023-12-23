using System.ComponentModel;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Microsoft.SemanticKernel;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.ComponentModel.DataAnnotations;

namespace Plugins;

public class Dalle3
{
    [KernelFunction, Description("Generate the URL of an image of an animal using DALL-E 3")]
    async public Task<string> ImageFromPrompt([Description("Prompt describing the image you want to generate")] string prompt)
    {   
        Console.WriteLine(prompt);
        HttpClient client = new HttpClient
        {
            BaseAddress = new Uri("https://api.openai.com/v1/")
        };

        var (apiKey, orgId) = Settings.LoadFromFile();

        client.DefaultRequestHeaders
            .Accept
            .Add(new MediaTypeWithQualityHeaderValue("application/json")); 
        
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
        client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

        var obj = new {
            model = "dall-e-3",
            prompt = prompt,
            n = 1,
            size = "1024x1024"};

        var content = new StringContent(JsonSerializer.Serialize(obj), Encoding.UTF8, "application/json");

        var response  = await client.PostAsync("images/generations", content);

        if (!response.IsSuccessStatusCode)
        {
            return $"Error: {response.StatusCode}";
        }

        string jsonString = await response.Content.ReadAsStringAsync();    
        using JsonDocument doc = JsonDocument.Parse(jsonString);
        JsonElement root = doc.RootElement;
        string url = root.GetProperty("data")[0]!.GetProperty("url")!.GetString()!;
        return url;
    }
}
