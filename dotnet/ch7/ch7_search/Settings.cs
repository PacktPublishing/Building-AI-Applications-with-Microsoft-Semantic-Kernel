using System.Text.Json;

public static class Settings {    
  public static (string apiKey, string? orgId, string? searchServiceName, string? searchServiceAdminKey, string? searchIndexName)
        LoadFromFile(string configFile = "config/settings.json")
    {
        if (!File.Exists(configFile))
        {
            Console.WriteLine("Configuration not found: " + configFile);
            throw new Exception("Configuration not found");
        }
        try
        {
            var config = JsonSerializer.Deserialize<Dictionary<string, string>>(File.ReadAllText(configFile));

            // check whether config is null
            if (config == null)
            {
                Console.WriteLine("Configuration is null");
                throw new Exception("Configuration is null");
            }

            string apiKey = config["apiKey"];

            
            string? orgId;

            // check whether orgId is in the file
            if (!config.ContainsKey("orgId"))
            {
                orgId = null;
            }
            else
            {
                orgId = config["orgId"];
            }

            string searchServiceName = config["ARXIV_SEARCH_SERVICE_NAME"];
            string searchServiceAdminKey = config["ARXIV_SEARCH_ADMIN_KEY"];
            string searchIndexName = config["ARXIV_SEARCH_INDEX_NAME"];

            return (apiKey, orgId, searchServiceName, searchServiceAdminKey, searchIndexName);

        }

        catch (Exception e)
        {
            Console.WriteLine("Something went wrong: " + e.Message);
            return ("", "", "", "", "");
        }
    }
}