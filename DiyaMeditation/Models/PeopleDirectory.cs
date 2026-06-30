using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;

namespace DiyaMeditation.Models;

/// <summary>
/// Loads the fixed list of people from a local CSV or XLSX file (offline, no network).
///
/// File location (first match wins):
///   1. DIYA_PEOPLE_FILE env var (full path)
///   2. ./people.csv or ./people.xlsx (current dir)
///   3. &lt;app&gt;/people.csv or &lt;app&gt;/people.xlsx (bundled sample)
///   4. ~/diya-people.csv or ~/diya-people.xlsx
///
/// Expected columns (header row, case-insensitive, any order):
///   Id, Name, Email, Age   (Id and Name are the important ones)
/// </summary>
public sealed class PeopleDirectory
{
    public IReadOnlyList<VisitorData> People { get; }
    public string? SourcePath { get; }
    public string? Error { get; }

    private PeopleDirectory(IReadOnlyList<VisitorData> people, string? sourcePath, string? error)
    {
        People = people;
        SourcePath = sourcePath;
        Error = error;
    }

    public static PeopleDirectory Load()
    {
        string? path;
        try
        {
            path = ResolveFile();
        }
        catch (Exception ex)
        {
            return new PeopleDirectory(Array.Empty<VisitorData>(), null, ex.Message);
        }

        if (path is null)
            return new PeopleDirectory(Array.Empty<VisitorData>(), null,
                "No people file found. Set DIYA_PEOPLE_FILE or place people.csv next to the app.");

        try
        {
            var people = path.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase)
                ? LoadXlsx(path)
                : LoadCsv(path);
            return new PeopleDirectory(people, path, null);
        }
        catch (Exception ex)
        {
            return new PeopleDirectory(Array.Empty<VisitorData>(), path, $"Could not read {path}: {ex.Message}");
        }
    }

    public VisitorData? FindById(string? id)
    {
        if (string.IsNullOrWhiteSpace(id)) return null;
        var key = id.Trim();
        return People.FirstOrDefault(p =>
            string.Equals(p.Id, key, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>Returns people whose name contains the query (case-insensitive).</summary>
    public IReadOnlyList<VisitorData> SearchByName(string? query)
    {
        if (string.IsNullOrWhiteSpace(query)) return Array.Empty<VisitorData>();
        var q = query.Trim();
        return People
            .Where(p => p.Name.Contains(q, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }

    // ---- file resolution ---------------------------------------------------

    private static string? ResolveFile()
    {
        var custom = Environment.GetEnvironmentVariable("DIYA_PEOPLE_FILE");
        if (!string.IsNullOrWhiteSpace(custom))
        {
            if (!File.Exists(custom))
                throw new FileNotFoundException($"DIYA_PEOPLE_FILE points to a missing file: {custom}");
            return custom;
        }

        var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        var candidates = new[]
        {
            Path.Combine(Directory.GetCurrentDirectory(), "people.csv"),
            Path.Combine(Directory.GetCurrentDirectory(), "people.xlsx"),
            Path.Combine(AppContext.BaseDirectory, "people.csv"),
            Path.Combine(AppContext.BaseDirectory, "people.xlsx"),
            Path.Combine(home, "diya-people.csv"),
            Path.Combine(home, "diya-people.xlsx"),
        };
        return candidates.FirstOrDefault(File.Exists);
    }

    // ---- CSV ---------------------------------------------------------------

    private static List<VisitorData> LoadCsv(string path)
    {
        var lines = File.ReadAllLines(path, Encoding.UTF8);
        var people = new List<VisitorData>();
        if (lines.Length == 0) return people;

        var header = ParseCsvLine(lines[0]);
        var idx = MapColumns(header);

        for (var i = 1; i < lines.Length; i++)
        {
            if (string.IsNullOrWhiteSpace(lines[i])) continue;
            var cells = ParseCsvLine(lines[i]);
            var person = BuildPerson(cells, idx);
            if (person is not null) people.Add(person);
        }
        return people;
    }

    private static List<string> ParseCsvLine(string line)
    {
        var result = new List<string>();
        var sb = new StringBuilder();
        var inQuotes = false;
        for (var i = 0; i < line.Length; i++)
        {
            var c = line[i];
            if (inQuotes)
            {
                if (c == '"')
                {
                    if (i + 1 < line.Length && line[i + 1] == '"') { sb.Append('"'); i++; }
                    else inQuotes = false;
                }
                else sb.Append(c);
            }
            else
            {
                if (c == '"') inQuotes = true;
                else if (c == ',') { result.Add(sb.ToString()); sb.Clear(); }
                else sb.Append(c);
            }
        }
        result.Add(sb.ToString());
        return result;
    }

    // ---- XLSX (ClosedXML) --------------------------------------------------

    private static List<VisitorData> LoadXlsx(string path)
    {
        using var wb = new ClosedXML.Excel.XLWorkbook(path);
        var ws = wb.Worksheets.First();
        var rows = ws.RangeUsed()?.RowsUsed().ToList();
        var people = new List<VisitorData>();
        if (rows is null || rows.Count == 0) return people;

        var header = rows[0].Cells().Select(c => c.GetString()).ToList();
        var idx = MapColumns(header);

        for (var i = 1; i < rows.Count; i++)
        {
            var cells = rows[i].Cells(1, header.Count).Select(c => c.GetString()).ToList();
            var person = BuildPerson(cells, idx);
            if (person is not null) people.Add(person);
        }
        return people;
    }

    // ---- shared mapping ----------------------------------------------------

    private readonly record struct ColumnMap(int Id, int Name, int Email, int Age);

    private static ColumnMap MapColumns(List<string> header)
    {
        int Find(params string[] names)
        {
            for (var i = 0; i < header.Count; i++)
            {
                var h = header[i].Trim().ToLowerInvariant();
                if (names.Contains(h)) return i;
            }
            return -1;
        }

        return new ColumnMap(
            Id: Find("id", "passid", "pass id", "code"),
            Name: Find("name", "full name", "fullname"),
            Email: Find("email", "gmail", "e-mail", "mail"),
            Age: Find("age"));
    }

    private static VisitorData? BuildPerson(List<string> cells, ColumnMap idx)
    {
        string Cell(int i) => i >= 0 && i < cells.Count ? cells[i].Trim() : "";

        var name = Cell(idx.Name);
        var id = Cell(idx.Id);

        // Need at least a name. If no explicit id, derive a stable one from the name.
        if (string.IsNullOrWhiteSpace(name) && string.IsNullOrWhiteSpace(id))
            return null;
        if (string.IsNullOrWhiteSpace(id))
            id = NormalizeId(name);

        var ageStr = Cell(idx.Age);
        int.TryParse(ageStr, NumberStyles.Integer, CultureInfo.InvariantCulture, out var age);

        return new VisitorData
        {
            Id = id,
            Name = string.IsNullOrWhiteSpace(name) ? id : name,
            Email = Cell(idx.Email),
            Age = age > 0 ? age : 0,
        };
    }

    /// <summary>Stable fallback id from a name (used only when no Id column exists).</summary>
    public static string NormalizeId(string name)
    {
        var sb = new StringBuilder();
        foreach (var c in name.ToUpperInvariant())
            if (char.IsLetterOrDigit(c)) sb.Append(c);
        return sb.Length > 0 ? sb.ToString() : "UNKNOWN";
    }
}
