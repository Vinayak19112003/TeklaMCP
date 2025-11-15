using System;
using Tekla.Structures.Model;
using Tekla.Structures.Geometry3d;

// Connection Template for Tekla OpenAPI
// Creates structural connections

private void CreateConnections()
{
    Console.WriteLine("Creating connections...");

    int connectionCount = 0;

    {% for connection in connections %}
    {
        // Connection: {{ connection.id }}
        // Type: {{ connection.type }}

        {% if connection.type == "base_plate" %}
        // Base plate connection handled in column creation
        {% elif connection.type == "moment" %}
        CreateMomentConnection("{{ connection.primary_element }}",
                             new string[] { {% for sec in connection.secondary_elements %}"{{ sec }}"{% if not loop.last %}, {% endif %}{% endfor %} });
        {% elif connection.type == "simple_shear" %}
        CreateSimpleShearConnection("{{ connection.primary_element }}",
                                  new string[] { {% for sec in connection.secondary_elements %}"{{ sec }}"{% if not loop.last %}, {% endif %}{% endfor %} });
        {% endif %}

        connectionCount++;
    }
    {% endfor %}

    Console.WriteLine($"Created {connectionCount} connections");
}

private void CreateMomentConnection(string primaryId, string[] secondaryIds)
{
    // ### TODO: USER MUST FILL THIS SECTION
    // Implement moment connection logic
    // - Find primary and secondary elements
    // - Create connection component
    // - Set bolt and weld parameters

    Console.WriteLine($"Creating moment connection for {primaryId}");
}

private void CreateSimpleShearConnection(string primaryId, string[] secondaryIds)
{
    // ### TODO: USER MUST FILL THIS SECTION
    // Implement simple shear connection
    // - Fin plate or end plate
    // - Bolt specification

    Console.WriteLine($"Creating shear connection for {primaryId}");
}
