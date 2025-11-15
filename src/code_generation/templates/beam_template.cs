using System;
using Tekla.Structures.Model;
using Tekla.Structures.Geometry3d;

// Beam Template for Tekla OpenAPI
// Creates structural beams

private void CreateBeams()
{
    Console.WriteLine("Creating beams...");

    int beamCount = 0;

    {% for beam in beams %}
    {
        Beam beam = new Beam();
        beam.Name = "{{ beam.id }}";
        beam.StartPoint = new Point({{ beam.start_point.x }}, {{ beam.start_point.y }}, {{ beam.start_point.z }});
        beam.EndPoint = new Point({{ beam.end_point.x }}, {{ beam.end_point.y }}, {{ beam.end_point.z }});
        beam.Profile.ProfileString = "{{ beam.profile.profile_string }}";
        beam.Material.MaterialString = "{{ beam.material.material_string }}";
        beam.Class = "{{ beam.class_ }}";
        beam.Position.Depth = Position.DepthEnum.MIDDLE;
        beam.Position.Plane = Position.DepthEnum.MIDDLE;
        beam.Position.Rotation = Position.RotationEnum.TOP;

        if (beam.Insert())
        {
            beamCount++;
        }
        else
        {
            Console.WriteLine("Failed to create beam {{ beam.id }}");
        }
    }
    {% endfor %}

    Console.WriteLine($"Created {beamCount} beams");
}

// ### TODO: USER MUST FILL THIS SECTION
// Add beam-to-column connection creation:
// - Simple shear connections
// - Moment connections
// - End plate connections
