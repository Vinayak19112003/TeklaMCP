# Common Tekla Patterns

## Creating Columns
```csharp
Beam column = new Beam();
column.StartPoint = new Point(x, y, 0);
column.EndPoint = new Point(x, y, height);
column.Profile.ProfileString = "UC305*305*198";
column.Material.MaterialString = "S355";
column.Position.Depth = Position.DepthEnum.MIDDLE;
column.Position.Plane = Position.PlaneEnum.MIDDLE;
column.Insert();
```

## Creating Beams
```csharp
Beam beam = new Beam();
beam.StartPoint = new Point(x1, y1, z);
beam.EndPoint = new Point(x2, y2, z);
beam.Profile.ProfileString = "IPE400";
beam.Material.MaterialString = "S355";
beam.Insert();
```

## Base Plate Connection
```csharp
Connection bp = new Connection();
bp.Name = "Base Plate";
bp.Number = 1;
bp.SetAttribute("BoltSize", "M24");
bp.SetPrimaryObject(column);
bp.Insert();
```

### TODO: USER MUST FILL THIS SECTION
Add patterns for:
- Moment connections
- Bracing
- Purlins
- Custom components
