# Tekla OpenAPI Reference

Quick reference for Tekla Structures OpenAPI

## Common Classes

### Model
```csharp
Model model = new Model();
if (model.GetConnectionStatus())
{
    // Connected to Tekla
}
model.CommitChanges();
```

### Grid
```csharp
Grid grid = new Grid();
GridPlane gridPlane = new GridPlane();
GridLine gridLine = new GridLine();
gridLine.Point = new Point(x, y, z);
gridLine.Direction = new Vector(dx, dy, dz);
gridLine.Label = "A";
```

### Beam (Column/Beam)
```csharp
Beam beam = new Beam();
beam.StartPoint = new Point(x1, y1, z1);
beam.EndPoint = new Point(x2, y2, z2);
beam.Profile.ProfileString = "HEA300";  // Use * not x
beam.Material.MaterialString = "S355";
beam.Position.Depth = Position.DepthEnum.MIDDLE;
beam.Insert();
```

### Position Enums
- `Position.DepthEnum`: FRONT, MIDDLE, BEHIND
- `Position.PlaneEnum`: LEFT, MIDDLE, RIGHT
- `Position.RotationEnum`: FRONT, TOP, BACK, BELOW

### TODO: USER MUST FILL THIS SECTION
Add more Tekla API references:
- Connection components
- Bolts and welds
- Custom components
- Model queries
