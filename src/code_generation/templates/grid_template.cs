using System;
using Tekla.Structures.Model;
using Tekla.Structures.Geometry3d;

// Grid Template for Tekla OpenAPI
// This template creates a grid system

private void CreateGrid()
{
    Console.WriteLine("Creating grid system...");

    Grid grid = new Grid();
    grid.Name = "{{ grid_name }}";

    // X-axis gridlines
    GridPlane gridPlaneX = new GridPlane();
    gridPlaneX.Label = "X";

    {% for line in x_lines %}
    {
        GridLine gridLine = new GridLine();
        gridLine.Point = new Point({{ line.coordinate }}, 0, 0);
        gridLine.Direction = new Vector(0, 1, 0);
        gridLine.Label = "{{ line.label }}";
        gridPlaneX.GridLines.Add(gridLine);
    }
    {% endfor %}

    // Y-axis gridlines
    GridPlane gridPlaneY = new GridPlane();
    gridPlaneY.Label = "Y";

    {% for line in y_lines %}
    {
        GridLine gridLine = new GridLine();
        gridLine.Point = new Point(0, {{ line.coordinate }}, 0);
        gridLine.Direction = new Vector(1, 0, 0);
        gridLine.Label = "{{ line.label }}";
        gridPlaneY.GridLines.Add(gridLine);
    }
    {% endfor %}

    grid.GridPlanes.Add(gridPlaneX);
    grid.GridPlanes.Add(gridPlaneY);

    if (grid.Insert())
    {
        Console.WriteLine("Grid created successfully");
    }
    else
    {
        Console.WriteLine("ERROR: Failed to create grid");
    }
}
