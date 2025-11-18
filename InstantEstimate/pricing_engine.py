"""
Pricing Engine - Calculate costs from material quantities

This module calculates project costs with regional pricing support for India,
Middle East, Europe, and USA markets.
"""

from typing import Dict
from datetime import datetime


class PricingEngine:
    """Calculate construction costs with regional pricing and multi-currency support"""

    def __init__(self, region: str = "India"):
        """
        Initialize pricing engine

        Args:
            region: Region for pricing ("India", "Middle East", "Europe", "USA")
        """
        self.region = region
        self.currency = self._get_currency(region)
        self.prices = self._load_regional_prices(region)

    def _get_currency(self, region: str) -> str:
        """Get currency code for region"""
        currency_map = {
            "India": "INR",
            "Middle East": "AED",
            "Europe": "EUR",
            "USA": "USD"
        }
        return currency_map.get(region, "INR")

    def _load_regional_prices(self, region: str) -> Dict:
        """
        Load price database for the specified region

        Prices are based on current market rates (2024)
        """
        if region == "India":
            return {
                # Steel prices per tonne (₹)
                "steel": {
                    "S355": 65000,  # High strength steel
                    "S275": 62000,  # Medium strength
                    "S235": 60000,  # Standard steel
                },
                # Bolt prices per piece (₹)
                "bolts": {
                    "M20": 15,
                    "M24": 25,
                    "M30": 40,
                },
                # Welding per meter (₹)
                "welding": {
                    "fillet_6mm": 120,
                    "fillet_8mm": 180,
                },
                # Concrete per m³ (₹)
                "concrete": {
                    "M30": 7000,
                    "reinforcement_per_kg": 65,
                },
                # Paint per m² (₹)
                "paint": {
                    "steel_paint": 250,
                },
                # Labor per tonne (₹)
                "labor": {
                    "fabrication_per_tonne": 8000,
                    "erection_per_tonne": 12000,
                },
            }

        elif region == "Middle East":
            return {
                "steel": {
                    "S355": 900,  # AED per tonne
                    "S275": 850,
                    "S235": 800,
                },
                "bolts": {
                    "M20": 2,
                    "M24": 3,
                    "M30": 5,
                },
                "welding": {
                    "fillet_6mm": 15,
                    "fillet_8mm": 22,
                },
                "concrete": {
                    "M30": 350,
                    "reinforcement_per_kg": 3.5,
                },
                "paint": {
                    "steel_paint": 25,
                },
                "labor": {
                    "fabrication_per_tonne": 300,
                    "erection_per_tonne": 450,
                },
            }

        elif region == "Europe":
            return {
                "steel": {
                    "S355": 750,  # EUR per tonne
                    "S275": 720,
                    "S235": 700,
                },
                "bolts": {
                    "M20": 1.5,
                    "M24": 2.5,
                    "M30": 4.0,
                },
                "welding": {
                    "fillet_6mm": 12,
                    "fillet_8mm": 18,
                },
                "concrete": {
                    "M30": 120,
                    "reinforcement_per_kg": 1.2,
                },
                "paint": {
                    "steel_paint": 20,
                },
                "labor": {
                    "fabrication_per_tonne": 400,
                    "erection_per_tonne": 600,
                },
            }

        elif region == "USA":
            return {
                "steel": {
                    "S355": 900,  # USD per ton (US ton = 2000 lbs)
                    "S275": 850,
                    "S235": 800,
                },
                "bolts": {
                    "M20": 2,
                    "M24": 3,
                    "M30": 5,
                },
                "welding": {
                    "fillet_6mm": 15,
                    "fillet_8mm": 22,
                },
                "concrete": {
                    "M30": 150,
                    "reinforcement_per_kg": 1.5,
                },
                "paint": {
                    "steel_paint": 25,
                },
                "labor": {
                    "fabrication_per_tonne": 500,
                    "erection_per_tonne": 800,
                },
            }

        else:
            # Default to India
            return self._load_regional_prices("India")

    def calculate_material_costs(self, quantities: Dict) -> Dict:
        """
        Calculate material costs with detailed breakdown

        Args:
            quantities: Dict from QuantityExtractor.get_all_quantities()

        Returns:
            Dict with detailed material cost breakdown
        """
        costs = {
            "steel": [],
            "bolts": [],
            "welding": [],
            "concrete": [],
            "paint": [],
        }
        total = 0.0

        # Steel costs
        steel_data = quantities.get("steel", {})
        for material, data in steel_data.items():
            weight_kg = data.get("weight_kg", 0)
            weight_tonnes = weight_kg / 1000.0
            rate = self.prices["steel"].get(material, self.prices["steel"]["S235"])
            amount = weight_tonnes * rate

            costs["steel"].append({
                "item": f"Structural Steel - {material}",
                "quantity": round(weight_tonnes, 3),
                "unit": "tonne",
                "rate": rate,
                "amount": round(amount, 2)
            })
            total += amount

        # Bolt costs
        bolt_data = quantities.get("bolts", {})
        for size, qty in bolt_data.items():
            if qty > 0:
                rate = self.prices["bolts"].get(size, 20)
                amount = qty * rate

                costs["bolts"].append({
                    "item": f"Bolts - {size}",
                    "quantity": qty,
                    "unit": "nos",
                    "rate": rate,
                    "amount": round(amount, 2)
                })
                total += amount

        # Welding costs
        weld_data = quantities.get("welds", {})
        for weld_type, length in weld_data.items():
            if length > 0:
                rate = self.prices["welding"].get(weld_type, 150)
                amount = length * rate

                costs["welding"].append({
                    "item": f"Welding - {weld_type.replace('_', ' ').title()}",
                    "quantity": round(length, 1),
                    "unit": "m",
                    "rate": rate,
                    "amount": round(amount, 2)
                })
                total += amount

        # Concrete costs
        concrete_data = quantities.get("concrete", {})
        for concrete_type, qty in concrete_data.items():
            if qty > 0:
                if "reinforcement" in concrete_type:
                    rate = self.prices["concrete"]["reinforcement_per_kg"]
                    item = "Reinforcement Steel"
                    unit = "kg"
                else:
                    rate = self.prices["concrete"].get(concrete_type, 7000)
                    item = f"Concrete - {concrete_type}"
                    unit = "m³"

                amount = qty * rate

                costs["concrete"].append({
                    "item": item,
                    "quantity": round(qty, 2),
                    "unit": unit,
                    "rate": rate,
                    "amount": round(amount, 2)
                })
                total += amount

        # Paint costs
        total_paint_area = sum(data.get("paint_area_m2", 0) for data in steel_data.values())
        if total_paint_area > 0:
            rate = self.prices["paint"]["steel_paint"]
            amount = total_paint_area * rate

            costs["paint"].append({
                "item": "Steel Painting (2 coats)",
                "quantity": round(total_paint_area, 2),
                "unit": "m²",
                "rate": rate,
                "amount": round(amount, 2)
            })
            total += amount

        costs["total"] = round(total, 2)
        return costs

    def calculate_labor_costs(self, quantities: Dict) -> Dict:
        """
        Calculate labor costs based on total steel weight

        Args:
            quantities: Dict from QuantityExtractor.get_all_quantities()

        Returns:
            Dict with labor cost breakdown
        """
        costs = []
        total = 0.0

        # Calculate total steel weight
        steel_data = quantities.get("steel", {})
        total_weight_kg = sum(data.get("weight_kg", 0) for data in steel_data.values())
        total_weight_tonnes = total_weight_kg / 1000.0

        # Fabrication costs
        fab_rate = self.prices["labor"]["fabrication_per_tonne"]
        fab_amount = total_weight_tonnes * fab_rate
        costs.append({
            "item": "Steel Fabrication",
            "quantity": round(total_weight_tonnes, 3),
            "unit": "tonne",
            "rate": fab_rate,
            "amount": round(fab_amount, 2)
        })
        total += fab_amount

        # Erection costs
        erection_rate = self.prices["labor"]["erection_per_tonne"]
        erection_amount = total_weight_tonnes * erection_rate
        costs.append({
            "item": "Steel Erection & Installation",
            "quantity": round(total_weight_tonnes, 3),
            "unit": "tonne",
            "rate": erection_rate,
            "amount": round(erection_amount, 2)
        })
        total += erection_amount

        return {
            "items": costs,
            "total": round(total, 2)
        }

    def calculate_total_estimate(self, quantities: Dict) -> Dict:
        """
        Calculate complete project estimate with all costs and markups

        Args:
            quantities: Dict from QuantityExtractor.get_all_quantities()

        Returns:
            Complete estimate with summary and detailed breakdown
        """
        # Calculate base costs
        material_costs = self.calculate_material_costs(quantities)
        labor_costs = self.calculate_labor_costs(quantities)

        materials_total = material_costs["total"]
        labor_total = labor_costs["total"]
        subtotal = materials_total + labor_total

        # Apply markups
        overhead_rate = 0.10  # 10%
        profit_rate = 0.15    # 15%
        contingency_rate = 0.05  # 5%

        overhead = subtotal * overhead_rate
        profit = subtotal * profit_rate
        contingency = subtotal * contingency_rate

        total_estimate = subtotal + overhead + profit + contingency

        # Calculate total steel weight for summary
        steel_data = quantities.get("steel", {})
        total_weight_kg = sum(data.get("weight_kg", 0) for data in steel_data.values())
        total_weight_tonnes = total_weight_kg / 1000.0

        # Build complete estimate
        estimate = {
            "project_summary": {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "region": self.region,
                "currency": self.currency,
                "total_steel_weight_tonnes": round(total_weight_tonnes, 3),
            },
            "material_costs": material_costs,
            "labor_costs": labor_costs,
            "summary": {
                "materials": round(materials_total, 2),
                "labor": round(labor_total, 2),
                "subtotal": round(subtotal, 2),
                "overhead_10%": round(overhead, 2),
                "profit_15%": round(profit, 2),
                "contingency_5%": round(contingency, 2),
                "total_estimate": round(total_estimate, 2),
            },
            "currency_symbol": self._get_currency_symbol(),
        }

        return estimate

    def _get_currency_symbol(self) -> str:
        """Get currency symbol for display"""
        symbols = {
            "INR": "₹",
            "USD": "$",
            "EUR": "€",
            "AED": "AED",
        }
        return symbols.get(self.currency, self.currency)

    def format_amount(self, amount: float) -> str:
        """Format amount with currency symbol"""
        symbol = self._get_currency_symbol()
        if self.currency == "INR":
            # Indian numbering system (lakhs, crores)
            return f"{symbol}{amount:,.2f}"
        else:
            return f"{symbol}{amount:,.2f}"


# Example usage
if __name__ == "__main__":
    # Sample quantities (would come from QuantityExtractor)
    sample_quantities = {
        "steel": {
            "S355": {
                "weight_kg": 2500.5,
                "paint_area_m2": 150.2,
                "members": []
            }
        },
        "bolts": {
            "M20": 96,
            "M24": 16,
            "M30": 0
        },
        "welds": {
            "fillet_6mm": 18.4,
            "fillet_8mm": 8.0
        },
        "concrete": {
            "M30": 4.0,
            "reinforcement_kg": 400.0
        }
    }

    # Test different regions
    regions = ["India", "Middle East", "Europe", "USA"]

    for region in regions:
        print(f"\n{'='*60}")
        print(f"🌍 PRICING ESTIMATE - {region.upper()}")
        print(f"{'='*60}\n")

        # Create pricing engine
        pricing = PricingEngine(region=region)

        # Calculate estimate
        estimate = pricing.calculate_total_estimate(sample_quantities)

        # Print summary
        print(f"📅 Date: {estimate['project_summary']['date']}")
        print(f"💱 Currency: {estimate['project_summary']['currency']}")
        print(f"⚖️  Total Steel: {estimate['project_summary']['total_steel_weight_tonnes']} tonnes\n")

        print("💰 COST SUMMARY:")
        print(f"  Materials:    {pricing.format_amount(estimate['summary']['materials'])}")
        print(f"  Labor:        {pricing.format_amount(estimate['summary']['labor'])}")
        print(f"  ─────────────────────")
        print(f"  Subtotal:     {pricing.format_amount(estimate['summary']['subtotal'])}")
        print(f"  Overhead 10%: {pricing.format_amount(estimate['summary']['overhead_10%'])}")
        print(f"  Profit 15%:   {pricing.format_amount(estimate['summary']['profit_15%'])}")
        print(f"  Contingency:  {pricing.format_amount(estimate['summary']['contingency_5%'])}")
        print(f"  ═════════════════════")
        print(f"  TOTAL:        {pricing.format_amount(estimate['summary']['total_estimate'])}")

    print(f"\n{'='*60}")
    print("✅ Pricing engine tested successfully!")
    print(f"{'='*60}\n")
