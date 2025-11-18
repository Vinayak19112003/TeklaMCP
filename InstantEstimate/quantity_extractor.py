"""
Quantity Extractor - Extract material quantities from structural JSON

This module extracts material quantities (steel, bolts, welds, concrete) from
structural building data for cost estimation.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class SectionProperties:
    """Properties of a steel section"""
    profile: str
    weight_per_meter: float  # kg/m
    paint_area_per_meter: float  # m²/m


class SectionDatabase:
    """Database of steel section properties with realistic values from steel tables"""

    def __init__(self):
        self.sections: Dict[str, SectionProperties] = {}
        self._load_sections()

    def _load_sections(self):
        """Load section properties for common European and British sections"""

        # HEA Sections (European Wide Flange - Light)
        hea_sections = {
            "HEA200": (42.3, 1.35),
            "HEA220": (50.5, 1.48),
            "HEA240": (60.3, 1.62),
            "HEA260": (68.2, 1.75),
            "HEA280": (76.4, 1.88),
            "HEA300": (88.3, 2.02),
            "HEA320": (97.6, 2.16),
            "HEA340": (105.0, 2.29),
            "HEA360": (112.0, 2.43),
            "HEA400": (125.0, 2.70),
            "HEA450": (140.0, 3.02),
            "HEA500": (155.0, 3.35),
            "HEA550": (166.0, 3.67),
            "HEA600": (178.0, 4.00),
        }

        # HEB Sections (European Wide Flange - Medium)
        heb_sections = {
            "HEB200": (61.3, 1.52),
            "HEB220": (71.5, 1.66),
            "HEB240": (83.2, 1.81),
            "HEB260": (93.0, 1.96),
            "HEB280": (103.0, 2.11),
            "HEB300": (117.0, 2.27),
            "HEB320": (127.0, 2.42),
            "HEB340": (134.0, 2.57),
            "HEB360": (142.0, 2.73),
            "HEB400": (155.0, 3.03),
            "HEB450": (171.0, 3.38),
            "HEB500": (187.0, 3.74),
            "HEB550": (199.0, 4.09),
            "HEB600": (212.0, 4.44),
        }

        # IPE Sections (European I-beams)
        ipe_sections = {
            "IPE200": (22.4, 0.91),
            "IPE220": (26.2, 1.02),
            "IPE240": (30.7, 1.13),
            "IPE270": (36.1, 1.29),
            "IPE300": (42.2, 1.46),
            "IPE330": (49.1, 1.62),
            "IPE360": (57.1, 1.79),
            "IPE400": (66.3, 2.01),
            "IPE450": (77.6, 2.28),
            "IPE500": (90.7, 2.55),
            "IPE550": (106.0, 2.86),
            "IPE600": (122.0, 3.17),
        }

        # UC Sections (British Universal Columns)
        uc_sections = {
            "UC152x152x23": (23.0, 0.88),
            "UC152x152x30": (30.0, 0.92),
            "UC203x203x46": (46.1, 1.28),
            "UC203x203x52": (52.0, 1.32),
            "UC203x203x60": (60.0, 1.37),
            "UC254x254x73": (73.1, 1.68),
            "UC254x254x89": (88.9, 1.76),
            "UC254x254x107": (107.0, 1.85),
            "UC305x305x97": (97.0, 2.08),
            "UC305x305x118": (118.0, 2.18),
            "UC305x305x137": (137.0, 2.28),
            "UC305x305x158": (158.0, 2.38),
            "UC305x305x198": (198.0, 2.54),
            "UC356x368x129": (129.0, 2.68),
            "UC356x368x153": (153.0, 2.80),
            "UC356x368x177": (177.0, 2.92),
            "UC356x406x235": (235.0, 3.35),
            "UC356x406x287": (287.0, 3.52),
            "UC356x406x340": (340.0, 3.68),
            "UC356x406x393": (393.0, 3.85),
            "UC356x406x467": (467.0, 4.08),
            "UC356x406x551": (551.0, 4.32),
            "UC356x406x634": (634.0, 4.56),
        }

        # UB Sections (British Universal Beams)
        ub_sections = {
            "UB203x133x25": (25.1, 0.88),
            "UB203x133x30": (30.0, 0.92),
            "UB254x146x31": (31.1, 1.08),
            "UB254x146x37": (37.0, 1.13),
            "UB254x146x43": (43.0, 1.18),
            "UB305x165x40": (40.3, 1.35),
            "UB305x165x46": (46.1, 1.40),
            "UB305x165x54": (54.1, 1.46),
            "UB356x171x45": (45.0, 1.52),
            "UB356x171x51": (51.0, 1.58),
            "UB356x171x57": (57.0, 1.63),
            "UB356x171x67": (67.1, 1.71),
            "UB457x191x67": (67.1, 1.95),
            "UB457x191x74": (74.3, 2.01),
            "UB457x191x82": (82.0, 2.07),
            "UB457x191x89": (89.3, 2.13),
            "UB533x210x82": (82.0, 2.30),
            "UB533x210x92": (92.1, 2.37),
            "UB533x210x101": (101.0, 2.44),
            "UB533x210x109": (109.0, 2.50),
            "UB610x229x101": (101.0, 2.68),
            "UB610x229x113": (113.0, 2.76),
            "UB610x229x125": (125.0, 2.84),
            "UB610x229x140": (140.0, 2.94),
            "UB686x254x125": (125.0, 3.10),
            "UB686x254x140": (140.0, 3.20),
            "UB686x254x152": (152.0, 3.28),
            "UB686x254x170": (170.0, 3.40),
            "UB762x267x134": (134.0, 3.48),
            "UB762x267x147": (147.0, 3.57),
            "UB762x267x173": (173.0, 3.73),
            "UB838x292x176": (176.0, 4.02),
            "UB838x292x194": (194.0, 4.13),
            "UB914x305x201": (201.0, 4.48),
            "UB914x305x224": (224.0, 4.61),
            "UB914x305x253": (253.0, 4.77),
            "UB914x419x343": (343.0, 5.68),
            "UB914x419x388": (388.0, 5.90),
        }

        # Load all sections
        for sections_dict in [hea_sections, heb_sections, ipe_sections, uc_sections, ub_sections]:
            for profile, (weight, paint_area) in sections_dict.items():
                self.sections[profile] = SectionProperties(
                    profile=profile,
                    weight_per_meter=weight,
                    paint_area_per_meter=paint_area
                )

    def get_section(self, profile: str) -> SectionProperties:
        """Get section properties by profile name"""
        # Normalize profile name (remove spaces, convert to uppercase)
        profile_normalized = profile.replace(" ", "").replace("*", "x").upper()

        if profile_normalized in self.sections:
            return self.sections[profile_normalized]

        # If not found, return default/estimated values
        print(f"⚠️  Warning: Section '{profile}' not in database, using estimated values")
        return SectionProperties(
            profile=profile,
            weight_per_meter=50.0,  # Estimated default
            paint_area_per_meter=1.5  # Estimated default
        )


class QuantityExtractor:
    """Extract material quantities from structural JSON for cost estimation"""

    def __init__(self):
        self.section_db = SectionDatabase()

    def extract_steel_quantities(self, structural_data: Dict) -> Dict[str, Dict]:
        """
        Extract steel quantities grouped by material grade

        Args:
            structural_data: Dict with 'columns', 'beams', 'bracing' arrays

        Returns:
            Dict grouped by material grade (S355, S275, S235) with weight, paint area, and member details
        """
        result = {}

        # Process columns
        columns = structural_data.get("columns", [])
        for col_data in columns:
            profile = col_data.get("profile", "HEA300")
            material = col_data.get("material", "S355")
            height = col_data.get("height", 8000)  # mm
            quantity = col_data.get("quantity", 1)

            # Get section properties
            section = self.section_db.get_section(profile)

            # Calculate quantities
            length_m = (height / 1000.0) * quantity
            weight_kg = section.weight_per_meter * length_m
            paint_area_m2 = section.paint_area_per_meter * length_m

            # Add to result
            if material not in result:
                result[material] = {
                    "weight_kg": 0.0,
                    "paint_area_m2": 0.0,
                    "members": []
                }

            result[material]["weight_kg"] += weight_kg
            result[material]["paint_area_m2"] += paint_area_m2
            result[material]["members"].append({
                "type": "Column",
                "profile": profile,
                "length_m": round(length_m, 2),
                "weight_kg": round(weight_kg, 2),
                "quantity": quantity
            })

        # Process beams
        beams = structural_data.get("beams", [])
        for beam_data in beams:
            profile = beam_data.get("profile", "IPE400")
            material = beam_data.get("material", "S355")
            length = beam_data.get("length", 10000)  # mm
            quantity = beam_data.get("quantity", 1)

            # Get section properties
            section = self.section_db.get_section(profile)

            # Calculate quantities
            length_m = (length / 1000.0) * quantity
            weight_kg = section.weight_per_meter * length_m
            paint_area_m2 = section.paint_area_per_meter * length_m

            # Add to result
            if material not in result:
                result[material] = {
                    "weight_kg": 0.0,
                    "paint_area_m2": 0.0,
                    "members": []
                }

            result[material]["weight_kg"] += weight_kg
            result[material]["paint_area_m2"] += paint_area_m2
            result[material]["members"].append({
                "type": "Beam",
                "profile": profile,
                "length_m": round(length_m, 2),
                "weight_kg": round(weight_kg, 2),
                "quantity": quantity
            })

        # Process bracing
        bracing = structural_data.get("bracing", [])
        for brace_data in bracing:
            profile = brace_data.get("profile", "L100x100x10")
            material = brace_data.get("material", "S275")
            length = brace_data.get("length", 8000)  # mm
            quantity = brace_data.get("quantity", 1)

            # Get section properties (use default for angles)
            section = self.section_db.get_section(profile)

            # Calculate quantities
            length_m = (length / 1000.0) * quantity
            weight_kg = section.weight_per_meter * length_m
            paint_area_m2 = section.paint_area_per_meter * length_m

            # Add to result
            if material not in result:
                result[material] = {
                    "weight_kg": 0.0,
                    "paint_area_m2": 0.0,
                    "members": []
                }

            result[material]["weight_kg"] += weight_kg
            result[material]["paint_area_m2"] += paint_area_m2
            result[material]["members"].append({
                "type": "Bracing",
                "profile": profile,
                "length_m": round(length_m, 2),
                "weight_kg": round(weight_kg, 2),
                "quantity": quantity
            })

        # Round totals
        for material in result:
            result[material]["weight_kg"] = round(result[material]["weight_kg"], 2)
            result[material]["paint_area_m2"] = round(result[material]["paint_area_m2"], 2)

        return result

    def extract_bolt_quantities(self, structural_data: Dict) -> Dict[str, int]:
        """
        Estimate bolt quantities based on connection count

        Rules:
        - Base plates: 4 bolts (M24) per column
        - Beam connections: 8 bolts (M20) per beam end (2 ends per beam)
        - Bracing: 4 bolts (M20) per brace connection (2 ends per brace)

        Returns:
            Dict with bolt sizes as keys and quantities as values
        """
        bolts = {"M20": 0, "M24": 0, "M30": 0}

        # Count columns for base plates
        columns = structural_data.get("columns", [])
        total_columns = sum(col.get("quantity", 1) for col in columns)
        bolts["M24"] += total_columns * 4  # 4 anchor bolts per column

        # Count beams for connections
        beams = structural_data.get("beams", [])
        total_beams = sum(beam.get("quantity", 1) for beam in beams)
        bolts["M20"] += total_beams * 16  # 8 bolts per end, 2 ends per beam

        # Count bracing
        bracing = structural_data.get("bracing", [])
        total_braces = sum(brace.get("quantity", 1) for brace in bracing)
        bolts["M20"] += total_braces * 8  # 4 bolts per end, 2 ends per brace

        return bolts

    def extract_weld_quantities(self, structural_data: Dict) -> Dict[str, float]:
        """
        Estimate weld quantities

        Rules:
        - Base plate welds: ~2m per column (fillet 8mm)
        - Beam stiffener welds: ~1m per beam connection (fillet 6mm)
        - Bracing gusset welds: ~0.8m per brace connection (fillet 6mm)

        Returns:
            Dict with weld types and lengths in meters
        """
        welds = {"fillet_6mm": 0.0, "fillet_8mm": 0.0}

        # Columns - base plate welds
        columns = structural_data.get("columns", [])
        total_columns = sum(col.get("quantity", 1) for col in columns)
        welds["fillet_8mm"] += total_columns * 2.0  # 2m per column base

        # Beams - stiffener and connection welds
        beams = structural_data.get("beams", [])
        total_beams = sum(beam.get("quantity", 1) for beam in beams)
        welds["fillet_6mm"] += total_beams * 2.0  # 1m per end, 2 ends

        # Bracing - gusset plate welds
        bracing = structural_data.get("bracing", [])
        total_braces = sum(brace.get("quantity", 1) for brace in bracing)
        welds["fillet_6mm"] += total_braces * 1.6  # 0.8m per end, 2 ends

        # Round to 1 decimal
        for weld_type in welds:
            welds[weld_type] = round(welds[weld_type], 1)

        return welds

    def extract_concrete_quantities(self, structural_data: Dict) -> Dict[str, float]:
        """
        Estimate concrete foundation quantities

        Rules:
        - Foundation: 1 m³ per column
        - Reinforcement: 100 kg/m³

        Returns:
            Dict with concrete grade and reinforcement quantities
        """
        concrete = {"M30": 0.0, "reinforcement_kg": 0.0}

        # Count columns for foundations
        columns = structural_data.get("columns", [])
        total_columns = sum(col.get("quantity", 1) for col in columns)

        concrete_volume = total_columns * 1.0  # 1 m³ per column
        concrete["M30"] = round(concrete_volume, 2)
        concrete["reinforcement_kg"] = round(concrete_volume * 100, 2)

        return concrete

    def get_all_quantities(self, structural_data: Dict) -> Dict:
        """
        Extract all quantities (steel, bolts, welds, concrete)

        Args:
            structural_data: Dict with structural building information

        Returns:
            Complete quantities dictionary with all materials
        """
        return {
            "steel": self.extract_steel_quantities(structural_data),
            "bolts": self.extract_bolt_quantities(structural_data),
            "welds": self.extract_weld_quantities(structural_data),
            "concrete": self.extract_concrete_quantities(structural_data)
        }


# Example usage
if __name__ == "__main__":
    # Sample structural data
    sample_data = {
        "project": {"name": "Industrial Warehouse"},
        "columns": [
            {"profile": "HEA300", "material": "S355", "height": 8000, "quantity": 4},
        ],
        "beams": [
            {"profile": "IPE400", "material": "S355", "length": 10000, "quantity": 6},
        ],
        "bracing": [
            {"profile": "L100x100x10", "material": "S275", "length": 8000, "quantity": 4},
        ]
    }

    # Create extractor
    extractor = QuantityExtractor()

    # Extract all quantities
    quantities = extractor.get_all_quantities(sample_data)

    # Print results
    print("🏗️  QUANTITY EXTRACTION RESULTS\n")

    print("📊 STEEL QUANTITIES:")
    for material, data in quantities["steel"].items():
        print(f"\n  {material}:")
        print(f"    Total Weight: {data['weight_kg']:.2f} kg ({data['weight_kg']/1000:.2f} tonnes)")
        print(f"    Paint Area: {data['paint_area_m2']:.2f} m²")
        print(f"    Members:")
        for member in data["members"]:
            print(f"      - {member['quantity']}x {member['type']} {member['profile']}: {member['length_m']:.2f}m, {member['weight_kg']:.2f} kg")

    print("\n🔩 BOLT QUANTITIES:")
    for size, qty in quantities["bolts"].items():
        if qty > 0:
            print(f"  {size}: {qty} nos")

    print("\n⚡ WELD QUANTITIES:")
    for weld_type, length in quantities["welds"].items():
        if length > 0:
            print(f"  {weld_type}: {length:.1f} m")

    print("\n🏗️  CONCRETE QUANTITIES:")
    for concrete_type, qty in quantities["concrete"].items():
        if qty > 0:
            if "reinforcement" in concrete_type:
                print(f"  Reinforcement: {qty:.2f} kg")
            else:
                print(f"  {concrete_type}: {qty:.2f} m³")

    print("\n✅ Quantity extraction completed successfully!")
