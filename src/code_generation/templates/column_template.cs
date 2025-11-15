using System;
using Tekla.Structures.Model;
using Tekla.Structures.Geometry3d;

// Column Template for Tekla OpenAPI
// Creates structural columns

private void CreateColumns()
{
    Console.WriteLine("Creating columns...");

    int columnCount = 0;

    {% for column in columns %}
    {
        Beam column = new Beam();
        column.Name = "{{ column.id }}";
        column.StartPoint = new Point({{ column.start_point.x }}, {{ column.start_point.y }}, {{ column.start_point.z }});
        column.EndPoint = new Point({{ column.end_point.x }}, {{ column.end_point.y }}, {{ column.end_point.z }});
        column.Profile.ProfileString = "{{ column.profile.profile_string }}";
        column.Material.MaterialString = "{{ column.material.material_string }}";
        column.Class = "{{ column.class_ }}";
        column.Position.Depth = Position.DepthEnum.MIDDLE;
        column.Position.Plane = Position.PlaneEnum.MIDDLE;
        column.Position.Rotation = Position.RotationEnum.FRONT;

        if (column.Insert())
        {
            columnCount++;
            // Create base plate for column
            CreateBasePlate(column);
        }
        else
        {
            Console.WriteLine("Failed to create column {{ column.id }}");
        }
    }
    {% endfor %}

    Console.WriteLine($"Created {columnCount} columns");
}

private void CreateBasePlate(Beam column)
{
    // Simple base plate connection
    // ### TODO: USER MUST FILL THIS SECTION
    // Customize base plate parameters:
    // - Plate thickness and size
    // - Bolt specification
    // - Connection component number

    try
    {
        Connection basePlate = new Connection();
        basePlate.Name = "Base Plate";
        basePlate.Number = 1;  // Standard base plate component
        basePlate.Code = "BP";
        basePlate.LoadAttributesFromFile("standard");

        basePlate.SetAttribute("BoltSize", "M24");
        basePlate.SetAttribute("BoltGrade", "8.8");
        basePlate.SetAttribute("BoltCount", 4);
        basePlate.SetAttribute("PlateThickness", 25.0);

        basePlate.SetPrimaryObject(column);

        if (!basePlate.Insert())
        {
            Console.WriteLine("Warning: Failed to create base plate");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Base plate error: {ex.Message}");
    }
}
