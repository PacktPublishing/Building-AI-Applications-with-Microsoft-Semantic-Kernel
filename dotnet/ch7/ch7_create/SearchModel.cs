using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
public class SearchModel
{
    [SimpleField(IsKey = true, IsSortable = true, IsFilterable = true, IsFacetable = true)]
    public string Id { get; set; }

    [SearchableField]
    public string AdditionalMetadata { get; set; }

    [SearchableField]
    public string Text { get; set; }

    [SearchableField]
    public string Description { get; set; }

    [SearchableField]
    public string ExternalSourceName { get; set; }

    [SimpleField(IsFilterable = true)]
    public bool IsReference { get; set; }

}
