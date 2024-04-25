using Microsoft.AspNetCore.Mvc;
namespace SkHomeAutomation.Controllers;
using Microsoft.Extensions.Logging;

public class LightOperationData
{
    public string? location { get; set; }
    public string? action { get; set; }
}

public class GarageOperationData
{
    public string? action { get; set; }
}

[ApiController]
[Route("[controller]")]
public class HomeAutomationController : ControllerBase
{

    private readonly ILogger<HomeAutomationController>? _logger;
    private HomeAutomation ha;

    public HomeAutomationController(ILogger<HomeAutomationController> logger)
    {
        _logger = logger;
        ha = new HomeAutomation();
    }

    [HttpPost("operate_light")]
    public IActionResult OperateLight([FromBody] LightOperationData data)
    {
        if (data.location == null || data.action == null)
        {
            return BadRequest("Location and action must be provided");
        }
        return Ok( ha.OperateLight(data.action, data.location) );
    }

    [HttpPost("operate_garage_door")]
    public IActionResult OperateGarageDoor([FromBody] GarageOperationData data)
    {
        if (data.action == null)
        {
            return BadRequest("Action must be provided");
        }
        return Ok( ha.OperateGarageDoor(data.action) );       
    }

}
