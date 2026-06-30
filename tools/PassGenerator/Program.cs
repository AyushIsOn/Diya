using System.Text;
using DiyaMeditation.Models;
using QRCoder;

// diya-passgen — generate one printable QR pass per person from the people list.
//
// Usage:
//   dotnet run -- [peopleFile] [outputDir]
//     peopleFile : path to people.csv / people.xlsx (default: ./people.csv)
//     outputDir  : where to write PNGs + index.html (default: ./passes)
//
// Each QR encodes the person's Id. The kiosk scans it and looks the Id up in the
// SAME people file, so the data must match.

var peopleFile = args.Length > 0 ? args[0] : "people.csv";
var outputDir = args.Length > 1 ? args[1] : "passes";

if (!File.Exists(peopleFile))
{
    Console.Error.WriteLine($"People file not found: {peopleFile}");
    return 1;
}

// PeopleDirectory resolves via DIYA_PEOPLE_FILE, so point it at the requested file.
Environment.SetEnvironmentVariable("DIYA_PEOPLE_FILE", Path.GetFullPath(peopleFile));
var dir = PeopleDirectory.Load();

if (dir.Error is not null)
{
    Console.Error.WriteLine($"Could not read people file: {dir.Error}");
    return 1;
}
if (dir.People.Count == 0)
{
    Console.Error.WriteLine("People file has no rows.");
    return 1;
}

Directory.CreateDirectory(outputDir);

var html = new StringBuilder();
html.AppendLine("<!doctype html><html><head><meta charset='utf-8'><title>Diya Passes</title>");
html.AppendLine("<style>body{font-family:sans-serif}.pass{display:inline-block;width:220px;margin:10px;padding:12px;border:1px solid #ccc;border-radius:10px;text-align:center;page-break-inside:avoid}.pass img{width:180px;height:180px}.n{font-weight:600;margin-top:6px}.i{color:#666;font-size:12px}</style>");
html.AppendLine("</head><body><h2>Diya Meditation — Entry Passes</h2>");

using var generator = new QRCodeGenerator();
var count = 0;
foreach (var p in dir.People)
{
    using var data = generator.CreateQrCode(p.Id, QRCodeGenerator.ECCLevel.M);
    var png = new PngByteQRCode(data).GetGraphic(10);

    var safe = new string(p.Name.Select(c => char.IsLetterOrDigit(c) ? c : '_').ToArray());
    var fileName = $"{p.Id}_{safe}.png";
    File.WriteAllBytes(Path.Combine(outputDir, fileName), png);

    html.AppendLine($"<div class='pass'><img src='{fileName}' alt='{p.Id}'/>" +
                    $"<div class='n'>{System.Net.WebUtility.HtmlEncode(p.Name)}</div>" +
                    $"<div class='i'>{System.Net.WebUtility.HtmlEncode(p.Id)}</div></div>");
    count++;
}

html.AppendLine("</body></html>");
File.WriteAllText(Path.Combine(outputDir, "index.html"), html.ToString());

Console.WriteLine($"Generated {count} passes in {Path.GetFullPath(outputDir)}");
Console.WriteLine($"Open {Path.Combine(outputDir, "index.html")} to print them all.");
return 0;
